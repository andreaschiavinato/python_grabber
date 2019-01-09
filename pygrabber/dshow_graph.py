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
import time

from pygrabber.dshow_structures import *
from pygrabber.dshow_ids import *
from pygrabber.win_api_extra import *
from comtypes.persist import IPropertyBag
from comtypes import *


class FilterGraph:

    def __init__(self):
        self.filter_graph = client.CreateObject(clsids.CLSID_FilterGraph, interface=qedit.IFilterGraph)
        self.capture_filter = None
        self.sample_grabber = None
        self.sample_grabber_cb = None
        self.render_filter = None
        self.image_resolution = None
        self.media_control = None
        self.media_event = None
        self.video_window = None

    def add_input_device(self, index):
        assert self.capture_filter is None
        self.capture_filter = _get_filter_by_index(DeviceCategories.CLSID_VideoInputDeviceCategory, index)
        self.filter_graph.AddFilter(self.capture_filter, _get_filter_name(self.capture_filter))

    def add_sample_grabber(self, callback):
        assert self.sample_grabber is None
        sample_grabber = _get_filter_by_CLSID(clsids.CLSID_SampleGrabber)
        sample_grabber_cast = sample_grabber.QueryInterface(ISampleGrabber)
        self.sample_grabber_cb = _sample_grabber_callback(callback)
        sample_grabber_cast.SetCallback(self.sample_grabber_cb, 1)
        sg_type = qedit._AMMediaType()
        sg_type.majortype = GUID(MediaTypes.Video)
        sg_type.subtype = GUID(MediaSubtypes.RGB24)
        sample_grabber_cast.SetMediaType(sg_type)
        self.filter_graph.AddFilter(sample_grabber, "Sample grabber")
        self.sample_grabber = sample_grabber

    def add_null_render(self):
        assert self.render_filter is None
        self.render_filter = _get_filter_by_CLSID(clsids.CLSID_NullRender)
        self.filter_graph.AddFilter(self.render_filter, "Render")

    def add_default_render(self):
        assert self.render_filter is None
        self.render_filter = _get_filter_by_CLSID(clsids.CLSID_VideoRendererDefault)
        self.filter_graph.AddFilter(self.render_filter, "Render")

    def add_video_mixing_render(self):
        assert self.render_filter is None
        self.render_filter = _get_filter_by_CLSID(clsids.CLSID_VideoMixingRenderer)
        self.filter_graph.AddFilter(self.render_filter, "Render")

    def prepare(self):
        assert self.capture_filter is not None
        assert self.render_filter is not None
        graph_builder = self.filter_graph.QueryInterface(qedit.IGraphBuilder)
        if self.sample_grabber is None:
            graph_builder.Connect(_get_pin(self.capture_filter, PIN_OUT), _get_pin(self.render_filter, PIN_IN))
        else:
            graph_builder.Connect(_get_pin(self.capture_filter, PIN_OUT), _get_pin(self.sample_grabber, PIN_IN))
            graph_builder.Connect(_get_pin(self.sample_grabber, PIN_OUT), _get_pin(self.render_filter, PIN_IN))
            self.sample_grabber_cb.image_resolution = self.get_sample_grabber_resolution()
        self.media_control = self.filter_graph.QueryInterface(quartz.IMediaControl)
        self.media_event = self.filter_graph.QueryInterface(quartz.IMediaEvent)

    def configure_render(self, handle):
        # must be called after the graph is connected
        self.video_window = self.render_filter.QueryInterface(IVideoWindow)
        self.video_window.put_Owner(handle)
        self.video_window.put_WindowStyle(WS_CHILD | WS_CLIPSIBLINGS)

    def update_window(self, width, height):
        if self.video_window is not None:
            img_w, img_h = self.get_sample_grabber_resolution()
            scale_w = width/img_w
            scale_h = height/img_h
            scale = min(scale_w, scale_h, 1)
            self.video_window.SetWindowPosition(0, 0, int(img_w*scale), int(img_h*scale))

    def run(self):
        self.media_control.Run()

    def stop(self):
        self.media_control.Stop()
        if self.video_window is not None:
            self.video_window.put_Visible(False)
            self.video_window.put_Owner(0)

    def pause(self):
        self.media_control.Pause()

    def get_state(self):
        return self.media_control.GetState(0xFFFFFFFF)  # 0xFFFFFFFF = infinite timeout

    def set_properties(self, filter):
        try:
            spec_pages = filter.QueryInterface(ISpecifyPropertyPages)
            cauuid = spec_pages.GetPages()
            if cauuid.element_count > 0:
                whandle = windll.user32.GetTopWindow(None)
                OleCreatePropertyFrame(
                    whandle,
                    0, 0, None,
                    1, byref(cast(filter, LPUNKNOWN)),
                    cauuid.element_count, cauuid.elements,
                    0, 0, None)
                windll.ole32.CoTaskMemFree(cauuid.elements)
        except COMError:
            pass

    def get_input_devices(self):
        return _get_available_filters(DeviceCategories.CLSID_VideoInputDeviceCategory)

    def get_formats(self):
        out_pin = _get_pin(self.capture_filter, PIN_OUT)
        stream_config = out_pin.QueryInterface(IAMStreamConfig)
        count, size = stream_config.GetNumberOfCapabilities()
        buffer = (c_ubyte * size)()
        result = []
        for i in range(0, count):
            media_type = stream_config.GetStreamCaps(i, buffer)
            p_video_info_header = cast(media_type.contents.pbFormat, POINTER(VIDEOINFOHEADER))
            bmp_header = p_video_info_header.contents.bmi_header
            if bmp_header.biWidth > 0 and bmp_header.biHeight > 0:
                result.append((
                    i,
                    subtypes[str(media_type.contents.subtype)],
                    bmp_header.biWidth,
                    bmp_header.biHeight,
                    bmp_header.biBitCount))
        return result

    def set_format(self, index):
        out_pin = _get_pin(self.capture_filter, PIN_OUT)
        stream_config = out_pin.QueryInterface(IAMStreamConfig)
        count, size = stream_config.GetNumberOfCapabilities()
        buffer = (c_ubyte * size)()
        media_type = stream_config.GetStreamCaps(index, buffer)
        stream_config.SetFormat(media_type)

    def get_sample_grabber_resolution(self):
        sample_grabber_cast = self.sample_grabber.QueryInterface(ISampleGrabber)
        media_type = sample_grabber_cast.GetConnectedMediaType()
        p_video_info_header = cast(media_type.pbFormat, POINTER(VIDEOINFOHEADER))
        bmp_header = p_video_info_header.contents.bmi_header
        return bmp_header.biWidth, bmp_header.biHeight

    def display_format_dialog(self):
        self.set_properties(_get_pin(self.capture_filter, PIN_OUT))

    def grab_frame(self):
        self.sample_grabber_cb.keep_photo = True

    def get_input_device(self):
        return self.capture_filter

    def remove_filters(self):
        enum_filters = self.filter_graph.EnumFilters()
        filt, count = enum_filters.Next(1)
        while count > 0:
            self.filter_graph.RemoveFilter(filt)
            enum_filters.Reset()
            filt, count = enum_filters.Next(1)


class _sample_grabber_callback(COMObject):
    _com_interfaces_ = [qedit.ISampleGrabberCB]

    def __init__(self, callback):
        self.callback = callback
        self.cnt = 0
        self.keep_photo = False
        self.image_resolution = None
        super(_sample_grabber_callback, self).__init__()

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


def _get_available_filters(category_clsid):
    system_device_enum = client.CreateObject(clsids.CLSID_SystemDeviceEnum, interface=ICreateDevEnum)
    filter_enumerator = system_device_enum.CreateClassEnumerator(GUID(category_clsid), dwFlags=0)
    moniker, count = filter_enumerator.Next(1)
    result = []
    while count > 0:
        result.append(_get_filter_name(moniker))
        moniker, count = filter_enumerator.Next(1)
    return result


def _get_filter_name(arg):
    if type(arg) == POINTER(IMoniker):
        property_bag = arg.BindToStorage(0, 0, IPropertyBag._iid_).QueryInterface(IPropertyBag)
        return property_bag.Read("FriendlyName", pErrorLog=None)
    elif type(arg) == POINTER(qedit.IBaseFilter):
        filter_info = arg.QueryFilterInfo()
        return wstring_at(filter_info.achName)
    else:
        return None


def _get_filter_by_index(category_clsid, index):
    system_device_enum = client.CreateObject(clsids.CLSID_SystemDeviceEnum, interface=ICreateDevEnum)
    filter_enumerator = system_device_enum.CreateClassEnumerator(GUID(category_clsid), dwFlags=0)
    if index > 0:
        _ = filter_enumerator.Next(index)
    moniker, _ = filter_enumerator.Next(1)
    return moniker.BindToObject(0, 0, qedit.IBaseFilter._iid_).QueryInterface(qedit.IBaseFilter)


def _get_filter_by_CLSID(clsid):
    return client.CreateObject(clsid, interface=qedit.IBaseFilter)


def _get_pin(filter, direction):
    # 0 = in, 1 = out
    enum = filter.EnumPins()
    pin, count = enum.Next(1)
    while count > 0:
        if pin.QueryDirection() == direction:
            return pin
        pin, count = enum.Next(1)
    return None


def print_graph_filters(filter_graph):
    print("Filters in graph:")
    enum_filters = filter_graph.EnumFilters()
    filt, count = enum_filters.Next(1)
    while count > 0:
        print(_get_filter_name(filt))
        filt, count = enum_filters.Next(1)
    print("---")


def print_filter_pins(filter):
    print(f"Pins of: {_get_filter_name(filter)}")
    enum = filter.EnumPins()
    pin, count = enum.Next(1)
    while count > 0:
        info = pin.QueryPinInfo()
        direction, name = (info.dir, wstring_at(info.achName))
        print(f"PIN {direction} - {name}")
        pin, count = enum.Next(1)
