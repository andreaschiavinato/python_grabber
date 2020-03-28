#
# python_grabber
#
# Authors:
#  Andrea Schiavinato <andrea.schiavinato84@gmail.com>
#
# Copyright (C) 2019 Andrea Schiavinato
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import numpy as np
import os.path
from enum import Enum
from comtypes.persist import IPropertyBag

from pygrabber.dshow_core import *
from pygrabber.windows_media import *
from pygrabber.dshow_ids import *
from pygrabber.win_api_extra import *


class StateGraph(Enum):
    Stopped = 0
    Paused = 1
    Running = 2


class RecordingFormat(Enum):
    AVI = 0
    ASF = 1


class FilterType(Enum):
    video_input = 0
    audio_input = 1
    video_compressor = 2
    audio_compressor = 3
    sample_grabber = 4
    render = 5
    file_sink = 6
    muxer = 7
    smart_tee = 8


class Filter:
    # Wrapper around a Direct Show filter
    def __init__(self, instance, name, capture_builder):
        self.instance = instance
        self.capture_builder = capture_builder
        self.Name = name
        self.out_pins = []
        self.in_pins = []
        self.reload_pins()

    def get_out(self):
        return self.out_pins[0]

    def get_in(self, index=0):
        return self.in_pins[index]

    def find_pin(self, direction, category=None, type=None, unconnected=True):
        try:
            return self.capture_builder.FindPin(self.instance, direction, category, type, unconnected, 0)
        except COMError:
            return None  # assuming preview pin not found

    def reload_pins(self):
        # 0 = in, 1 = out
        self.out_pins = []
        self.in_pins = []
        enum = self.instance.EnumPins()
        pin, count = enum.Next(1)
        while count > 0:
            if pin.QueryDirection() == 0:
                self.in_pins.append(pin)
            else:
                self.out_pins.append(pin)
            pin, count = enum.Next(1)

    def set_properties(self):
        show_properties(self.instance)

    def get_name(self):
        filter_info = self.instance.QueryFilterInfo()
        return wstring_at(filter_info.achName)

    def print_info(self):
        print(f"Pins of: {self.get_name()}")
        enum = self.instance.EnumPins()
        pin, count = enum.Next(1)
        while count > 0:
            info = pin.QueryPinInfo()
            direction, name = (info.dir, wstring_at(info.achName))
            print(f"PIN {'in' if direction == 0 else 'out'} - {name}")
            pin, count = enum.Next(1)


class VideoInput(Filter):
    def __init__(self, args, capture_builder):
        Filter.__init__(self, args[0], args[1], capture_builder)

    def get_current_format(self):
        stream_config = self.get_out().QueryInterface(IAMStreamConfig)
        media_type = stream_config.GetFormat()
        p_video_info_header = cast(media_type.contents.pbFormat, POINTER(VIDEOINFOHEADER))
        bmp_header = p_video_info_header.contents.bmi_header
        return bmp_header.biWidth, bmp_header.biHeight

    def get_formats(self):
        # https://docs.microsoft.com/en-us/windows/win32/directshow/configure-the-video-output-format
        stream_config = self.get_out().QueryInterface(IAMStreamConfig)
        media_types_count, _ = stream_config.GetNumberOfCapabilities()
        result = []
        for i in range(0, media_types_count):
            media_type, capability = stream_config.GetStreamCaps(i)
            p_video_info_header = cast(media_type.contents.pbFormat, POINTER(VIDEOINFOHEADER))
            bmp_header = p_video_info_header.contents.bmi_header
            result.append({
                'index': i,
                'media_type_str': subtypes[str(media_type.contents.subtype)],
                'width': bmp_header.biWidth,
                'height': bmp_header.biHeight,
                'min_framerate': 10000000 / capability.MinFrameInterval,
                'max_framerate': 10000000 / capability.MaxFrameInterval
            })
            #print(f"{capability.MinOutputSize.cx}x{capability.MinOutputSize.cx} - {capability.MaxOutputSize.cx}x{capability.MaxOutputSize.cx}")
        return result

    def set_format(self, format_index):
        stream_config = self.get_out().QueryInterface(IAMStreamConfig)
        media_type, _ = stream_config.GetStreamCaps(format_index)
        stream_config.SetFormat(media_type)

    def show_format_dialog(self):
        show_properties(self.get_out())


class AudioInput(Filter):
    def __init__(self, args, capture_builder):
        Filter.__init__(self, args[0], args[1], capture_builder)


class VideoCompressor(Filter):
    def __init__(self, args, capture_builder):
        Filter.__init__(self, args[0], args[1], capture_builder)


class AudioCompressor(Filter):
    def __init__(self, args, capture_builder):
        Filter.__init__(self, args[0], args[1], capture_builder)


class Render(Filter):
    def __init__(self, instance, capture_builder):
        Filter.__init__(self, instance, "Render", capture_builder)
        try:
            self.video_window = self.instance.QueryInterface(IVideoWindow)
        except COMError:
            self.video_window = None # probably interface IVideoWindow not supported because using NullRender

    def configure_video_window(self, handle):
        # must be called after the graph is connected
        self.video_window.put_Owner(handle)
        self.video_window.put_WindowStyle(WS_CHILD | WS_CLIPSIBLINGS)

    def set_window_position(self, x, y, width, height):
        self.video_window.SetWindowPosition(x, y, width, height)


class SampleGrabber(Filter):
    def __init__(self, capture_builder):
        Filter.__init__(self, client.CreateObject(GUID(clsids.CLSID_SampleGrabber), interface=qedit.IBaseFilter), "Sample Grabber", capture_builder)
        self.sample_grabber = self.instance.QueryInterface(ISampleGrabber)
        self.callback = None

    def set_callback(self, callback, which_method_to_callback):
        self.callback = callback
        self.sample_grabber.SetCallback(callback, which_method_to_callback)

    def set_media_type(self, media_type, media_subtype):
        sg_type = qedit._AMMediaType()
        sg_type.majortype = GUID(media_type)
        sg_type.subtype = GUID(media_subtype)
        self.sample_grabber.SetMediaType(sg_type)

    def get_resolution(self):
        media_type = self.sample_grabber.GetConnectedMediaType()
        p_video_info_header = cast(media_type.pbFormat, POINTER(VIDEOINFOHEADER))
        bmp_header = p_video_info_header.contents.bmi_header
        return bmp_header.biWidth, bmp_header.biHeight

    def initialize_after_connection(self):
        self.callback.image_resolution = self.get_resolution()


class SmartTee(Filter):
    def __init__(self, capture_builder):
        Filter.__init__(self, client.CreateObject(GUID(clsids.CLSID_SmartTee),interface=qedit.IBaseFilter), "Smart Tee", capture_builder)


class Muxer(Filter):
    def __init__(self, args, capture_builder):
        Filter.__init__(self, args, "Muxer", capture_builder)


class SystemDeviceEnum:
    def __init__(self):
        self.system_device_enum = client.CreateObject(clsids.CLSID_SystemDeviceEnum, interface=ICreateDevEnum)

    def get_available_filters(self, category_clsid):
        filter_enumerator = self.system_device_enum.CreateClassEnumerator(GUID(category_clsid), dwFlags=0)
        moniker, count = filter_enumerator.Next(1)
        result = []
        while count > 0:
            result.append(get_moniker_name(moniker))
            moniker, count = filter_enumerator.Next(1)
        return result

    def get_filter_by_index(self, category_clsid, index):
        filter_enumerator = self.system_device_enum.CreateClassEnumerator(GUID(category_clsid), dwFlags=0)
        moniker, count = filter_enumerator.Next(1)
        i = 0
        while i != index and count > 0:
            moniker, count = filter_enumerator.Next(1)
            i = i + 1

        return moniker.BindToObject(0, 0, qedit.IBaseFilter._iid_).QueryInterface(qedit.IBaseFilter), \
               get_moniker_name(moniker)


class FilterFactory:
    def __init__(self, system_device_enum, capture_builder):
        self.system_device_enum = system_device_enum
        self.capture_builder = capture_builder

    def build_filter(self, filter_type, id):
        if filter_type == FilterType.video_input:
            return VideoInput(self.system_device_enum.get_filter_by_index(DeviceCategories.VideoInputDevice, id), self.capture_builder)
        elif filter_type == FilterType.audio_input:
            return AudioInput(self.system_device_enum.get_filter_by_index(DeviceCategories.AudioInputDevice, id), self.capture_builder)
        elif filter_type == FilterType.video_compressor:
            return VideoCompressor(self.system_device_enum.get_filter_by_index(DeviceCategories.VideoCompressor, id), self.capture_builder)
        elif filter_type == FilterType.audio_compressor:
            return AudioCompressor(self.system_device_enum.get_filter_by_index(DeviceCategories.AudioCompressor, id), self.capture_builder)
        elif filter_type == FilterType.render:
            return Render(client.CreateObject(GUID(id), interface=qedit.IBaseFilter), self.capture_builder)
        elif filter_type == FilterType.sample_grabber:
            return SampleGrabber(self.capture_builder)
        elif filter_type == FilterType.muxer:
            return Muxer(id, self.capture_builder)
        elif filter_type == FilterType.smart_tee:
            return SmartTee(self.capture_builder)
        else:
            raise ValueError('Cannot create filter', filter_type, id)


class MediaType:
    def __init__(self, majortype_guid, subtype_guid):
        self.instance = qedit._AMMediaType()
        self.instance.majortype = GUID(majortype_guid)
        self.instance.subtype = GUID(subtype_guid)


class WmProfileManager:
    def __init__(self):
        self.profile_manager = POINTER(IWMProfileManager2)()
        WMCreateProfileManager(byref(self.profile_manager))
        self.profile_manager.SetSystemProfileVersion(0x00080000)
        self.profiles, self.profiles_names = self.__load_profiles()

    def __load_profiles(self):
        nr_profiles = self.profile_manager.GetSystemProfileCount()
        profiles = [self.profile_manager.LoadSystemProfile(i) for i in range(0, nr_profiles)]
        profiles_names = []
        buf = create_unicode_buffer(200)
        for profile in profiles:
            i = DWORD(200)
            profile.GetName(buf, pointer(i))
            profiles_names.append(buf.value)
        return profiles, profiles_names


class FilterGraph:
    def __init__(self):
        self.filter_graph = client.CreateObject(clsids.CLSID_FilterGraph, interface=qedit.IFilterGraph)
        self.graph_builder = self.filter_graph.QueryInterface(qedit.IGraphBuilder)
        self.media_control = self.filter_graph.QueryInterface(quartz.IMediaControl)
        self.media_event = self.filter_graph.QueryInterface(quartz.IMediaEvent)
        self.capture_builder = client.CreateObject(clsids.CLSID_CaptureGraphBuilder2, interface=ICaptureGraphBuilder2)
        self.capture_builder.SetFiltergraph(self.filter_graph)

        self.system_device_enum = SystemDeviceEnum()
        self.filter_factory = FilterFactory(self.system_device_enum, self.capture_builder)
        self.wm_profile_manager = WmProfileManager()

        self.filters = {}
        self.recording_format = None
        self.is_recording = False

    def __add_filter(self, filter_type, filter_id):
        assert not(filter_type in self.filters)
        filter = self.filter_factory.build_filter(filter_type, filter_id)
        self.filters[filter_type] = filter
        self.filter_graph.AddFilter(filter.instance, filter.Name)

    def add_video_input_device(self, index):
        self.__add_filter(FilterType.video_input, index)

    def add_audio_input_device(self, index):
        self.__add_filter(FilterType.audio_input, index)

    def add_video_compressor(self, index):
        self.__add_filter(FilterType.video_compressor, index)

    def add_audio_compressor(self, index):
        self.__add_filter(FilterType.audio_compressor, index)

    def add_sample_grabber(self, callback):
        self.__add_filter(FilterType.sample_grabber, None)
        sample_grabber = self.filters[FilterType.sample_grabber]
        sample_grabber_cb = SampleGrabberCallback(callback)
        sample_grabber.set_callback(sample_grabber_cb, 1)
        sample_grabber.set_media_type(MediaTypes.Video, MediaSubtypes.RGB24)

    def add_null_render(self):
        self.__add_filter(FilterType.render, clsids.CLSID_NullRender)

    def add_default_render(self):
        self.__add_filter(FilterType.render, clsids.CLSID_VideoRendererDefault)

    def add_video_mixing_render(self):
        self.__add_filter(FilterType.render, clsids.CLSID_VideoMixingRenderer)

    def add_file_writer_and_muxer(self, filename):
        extension = os.path.splitext(filename)[1].upper()
        mediasubtype = MediaSubtypes.ASF if extension == ".WMV" else MediaSubtypes.AVI
        self.recording_format = RecordingFormat.ASF if extension == ".WMV" else RecordingFormat.AVI
        mux, filesink = self.capture_builder.SetOutputFileName(GUID(mediasubtype), filename)
        self.filters[FilterType.muxer] = self.filter_factory.build_filter(FilterType.muxer, mux)

    def configure_asf_compressor(self):
        pass
        # asf_config = self.mux.QueryInterface(IConfigAsfWriter)
        # print(asf_config.GetCurrentProfileGuid())
        #profile = asf_config.GetCurrentProfile()

    def prepare_preview_graph(self):
        assert FilterType.video_input in self.filters
        assert FilterType.render in self.filters
        if FilterType.sample_grabber not in self.filters:
            self.graph_builder.Connect(self.filters[FilterType.video_input].get_out(),
                                       self.filters[FilterType.render].get_in())
        else:
            self.graph_builder.Connect(self.filters[FilterType.video_input].get_out(),
                                       self.filters[FilterType.sample_grabber].get_in())
            self.graph_builder.Connect(self.filters[FilterType.sample_grabber].get_out(),
                                       self.filters[FilterType.render].get_in())
            self.filters[FilterType.sample_grabber].initialize_after_connection()
        self.is_recording = False

    def __get_capture_and_preview_pins(self):
        preview_pin = self.filters[FilterType.video_input].find_pin(PIN_OUT, category=GUID(PinCategory.Preview))
        capture_pin = self.filters[FilterType.video_input].find_pin(PIN_OUT, category=GUID(PinCategory.Capture))

        if (preview_pin is None) or (capture_pin is None):
            self.__add_filter(FilterType.smart_tee, None)
            smart_tee = self.filters[FilterType.smart_tee]
            self.graph_builder.Connect(capture_pin if capture_pin is not None else preview_pin, smart_tee.get_in())
            # assuming the 1st output pin of the smart tee filter is always the capture one
            capture_pin, preview_pin = smart_tee.out_pins

        return preview_pin, capture_pin

    def prepare_recording_graph(self):
        #  in theory we could use self.capture_builder.RenderStream,
        #  but it is not working when including the video compressor :-(
        assert FilterType.video_input in self.filters
        assert FilterType.render in self.filters
        assert FilterType.muxer in self.filters

        preview_pin, capture_pin = self.__get_capture_and_preview_pins()

        if self.recording_format == RecordingFormat.ASF:
            self.graph_builder.Connect(capture_pin,
                                       self.filters[FilterType.muxer].get_in(1))
            self.graph_builder.Connect(self.filters[FilterType.audio_input].get_out(),
                                       self.filters[FilterType.muxer].get_in(0))
            self.graph_builder.Connect(preview_pin, self.filters[FilterType.render].get_in())

        else:
            self.graph_builder.Connect(capture_pin, self.filters[FilterType.video_compressor].get_in())
            self.graph_builder.Connect(self.filters[FilterType.video_compressor].get_out(),
                                       self.filters[FilterType.muxer].get_in())
            self.graph_builder.Connect(preview_pin, self.filters[FilterType.render].get_in())

            if FilterType.audio_input in self.filters:
                self.graph_builder.Connect(self.filters[FilterType.audio_input].get_out(),
                                           self.filters[FilterType.audio_compressor].get_in())
                self.filters[FilterType.muxer].reload_pins()
                # when you connect an input pin of the muxer, an additional input pin is added
                self.graph_builder.Connect(self.filters[FilterType.audio_compressor].get_out(),
                                           self.filters[FilterType.muxer].get_in(1))

        self.is_recording = True

    def configure_render(self, handle):
        self.filters[FilterType.render].configure_video_window(handle)

    def update_window(self, width, height):
        if FilterType.render in self.filters:
            img_w, img_h = self.filters[FilterType.video_input].get_current_format()
            scale_w = width / img_w
            scale_h = height / img_h
            scale = min(scale_w, scale_h, 1)
            self.filters[FilterType.render].set_window_position(0, 0, int(img_w * scale), int(img_h * scale))

    def run(self):
        self.media_control.Run()

    def stop(self):
        if self.media_control is not None:
            # calling stop without calling prepare
            self.media_control.Stop()
        # if self.video_window is not None:
            # self.video_window.put_Visible(False)
            # self.video_window.put_Owner(0)

    def pause(self):
        self.media_control.Pause()

    def get_state(self):
        return StateGraph(self.media_control.GetState(0xFFFFFFFF))  # 0xFFFFFFFF = infinite timeout

    def get_input_devices(self):
        return self.system_device_enum.get_available_filters(DeviceCategories.VideoInputDevice)

    def get_audio_devices(self):
        return self.system_device_enum.get_available_filters(DeviceCategories.AudioInputDevice)

    def get_video_compressors(self):
        return self.system_device_enum.get_available_filters(DeviceCategories.VideoCompressor)

    def get_audio_compressors(self):
        return self.system_device_enum.get_available_filters(DeviceCategories.AudioCompressor)

    def get_asf_profiles(self):
        return self.wm_profile_manager.profiles_names

    def grab_frame(self):
        if FilterType.sample_grabber in self.filters:
            self.filters[FilterType.sample_grabber].callback.grab_frame()
            return True
        else:
            return False

    def get_input_device(self):
        return self.filters[FilterType.video_input]

    def remove_filters(self):
        enum_filters = self.filter_graph.EnumFilters()
        filt, count = enum_filters.Next(1)
        while count > 0:
            self.filter_graph.RemoveFilter(filt)
            enum_filters.Reset()
            filt, count = enum_filters.Next(1)
        self.filters = {}

    def remove_all_filters_but_video_source(self):
        video_input = self.filters[FilterType.video_input]
        enum_filters = self.filter_graph.EnumFilters()
        filters_to_delete = []
        filt, count = enum_filters.Next(1)
        while count > 0:
            if filt != video_input.instance:
                filters_to_delete.append(filt)
            filt, count = enum_filters.Next(1)
        for filt in filters_to_delete:
            self.filter_graph.RemoveFilter(filt)
        self.filters = {FilterType.video_input: video_input}

    def print_debug_info(self):
        helper = FilterGraphDebugHelper(self.filter_graph)
        helper.print_graph_info()


class FilterGraphDebugHelper:

    def __init__(self, filter_graph):
        self.filter_graph = filter_graph

    def print_graph_info(self):
        enum_filters = self.filter_graph.EnumFilters()
        filt, count = enum_filters.Next(1)
        while count > 0:
            filterName = self.get_filter_name(filt)
            print(f"FILTER {filterName} [{filt}]")

            enum_pins = filt.EnumPins()
            pin, count = enum_pins.Next(1)
            while count > 0:
                pin_name, direction, connected_pin, owner = self.get_pin_info(pin)
                if connected_pin is not None:
                    connected_pin_name, _, _, connected_filter = self.get_pin_info(connected_pin)
                    connected_filter_name = self.get_filter_name(connected_filter)

                print(f" - PIN {pin_name} {'in' if direction == 0 else 'out'} - Connected to: {connected_filter_name} [{pin}]")

                pin, count = enum_pins.Next(1)
            filt, count = enum_filters.Next(1)

    def get_filter_name(self, filter):
        filter_info = filter.QueryFilterInfo()
        return wstring_at(filter_info.achName)

    def get_pin_info(self, pin):
        info = pin.QueryPinInfo()
        name = wstring_at(info.achName)
        owner_filter = info.pFilter
        try:
            connected_pin = pin.ConnectedTo()
        except:
            connected_pin = None
        return name, info.dir, connected_pin, owner_filter


class SampleGrabberCallback(COMObject):
    _com_interfaces_ = [qedit.ISampleGrabberCB]

    def __init__(self, callback):
        self.callback = callback
        self.cnt = 0
        self.keep_photo = False
        self.image_resolution = None
        super(SampleGrabberCallback, self).__init__()

    def grab_frame(self):
        self.keep_photo = True

    def SampleCB(self, this, SampleTime, pSample):
        return 0

    def BufferCB(self, this, SampleTime, pBuffer, BufferLen):
        if self.keep_photo:
            self.keep_photo = False
            img = np.ctypeslib.as_array(pBuffer, shape=(self.image_resolution[1], self.image_resolution[0], 3))
            img = np.flip(np.copy(img), axis=0)
            self.callback(img)
        return 0

    # ALTERNATIVE
    # def BufferCB(self, this, SampleTime, pBuffer, BufferLen):
    #     if self.keep_photo:
    #         self.keep_photo = False
    #         bsize = self.image_resolution[1] *self.image_resolution[0] * 3
    #         img = pBuffer[:bsize]
    #         img = np.reshape(img, (self.image_resolution[1], self.image_resolution[0], 3))
    #         img = np.flip(img, axis=0)
    #         self.callback(img)
    #     return 0


def get_moniker_name(moniker):
    property_bag = moniker.BindToStorage(0, 0, IPropertyBag._iid_).QueryInterface(IPropertyBag)
    return property_bag.Read("FriendlyName", pErrorLog=None)


def show_properties(object):
    try:
        spec_pages = object.QueryInterface(ISpecifyPropertyPages)
        cauuid = spec_pages.GetPages()
        if cauuid.element_count > 0:
            whandle = windll.user32.GetTopWindow(None)
            OleCreatePropertyFrame(
                whandle,
                0, 0, None,
                1, byref(cast(object, LPUNKNOWN)),
                cauuid.element_count, cauuid.elements,
                0, 0, None)
            windll.ole32.CoTaskMemFree(cauuid.elements)
    except COMError:
        pass
