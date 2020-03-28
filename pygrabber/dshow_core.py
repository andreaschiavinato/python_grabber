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

# see https://github.com/tpn/winsdk-10/blob/master/Include/10.0.16299.0/um/axextend.idl for interface spec.

from pygrabber.moniker import *
from pygrabber.win_common_types import *
from comtypes import *
from comtypes import client
from ctypes.wintypes import RECT, SIZE, ULONG, LPOLESTR, DWORD, LONG
from comtypes.automation import IDispatch
from ctypes import c_int, c_long, c_longlong

qedit = client.GetModule("qedit.dll")
quartz = client.GetModule("quartz.dll")


PIN_IN = 0
PIN_OUT = 1


class BITMAPINFOHEADER(Structure):
    _fields_ = [
        ('biSize', c_uint32),
        ('biWidth', c_int),
        ('biHeight', c_int),
        ('biPlanes', c_short),
        ('biBitCount', c_short),
        ('biCompression', c_uint32),
        ('biSizeImage', c_uint32),
        ('biXPelsPerMeter', c_long),
        ('biYPelsPerMeter', c_long),
        ('biClrUsed', c_uint32),
        ('biClrImportant', c_uint32)
    ]


class VIDEOINFOHEADER(Structure):
    _fields_ = (
        ('source', RECT),
        ('target', RECT),
        ('bit_rate', DWORD),
        ('bit_error_rate', DWORD),
        ('avg_time_per_frame', REFERENCE_TIME),
        ('bmi_header', BITMAPINFOHEADER),
    )


class VIDEO_STREAM_CONFIG_CAPS(Structure):
    _fields_ = (
        ('guid', GUID),
        ('VideoStandard', ULONG),
        ('InputSize', SIZE),
        ('MinCroppingSize', SIZE),
        ('MaxCroppingSize', SIZE),
        ('CropGranularityX', c_int),
        ('CropGranularityY', c_int),
        ('CropAlignX', c_int),
        ('CropAlignY', c_int),
        ('MinOutputSize', SIZE),
        ('MaxOutputSize', SIZE),
        ('OutputGranularityX', c_int),
        ('OutputGranularityX', c_int),
        ('StretchTapsX', c_int),
        ('StretchTapsY', c_int),
        ('ShrinkTapsX', c_int),
        ('ShrinkTapsY', c_int),
        ('MinFrameInterval', c_longlong),
        ('MaxFrameInterval', c_longlong),
        ('MinBitsPerSecond', LONG),
        ('MaxBitsPerSecond', LONG)
    )


class ISampleGrabber(IUnknown):
    _case_insensitive_ = True
    'ISampleGrabber Interface'
    _iid_ = GUID('{6B652FFF-11FE-4FCE-92AD-0266B5D7C78F}')
    _idlflags_ = []


ISampleGrabber._methods_ = [
    COMMETHOD([], HRESULT, 'SetOneShot',
              ([], c_int, 'OneShot')),
    COMMETHOD([], HRESULT, 'SetMediaType',
              ([], POINTER(qedit._AMMediaType), 'pType')),
    COMMETHOD([], HRESULT, 'GetConnectedMediaType',
              (['out'], POINTER(qedit._AMMediaType), 'pType')),
    COMMETHOD([], HRESULT, 'SetBufferSamples',
              ([], c_int, 'BufferThem')),
    COMMETHOD([], HRESULT, 'GetCurrentBuffer',
              (['in', 'out'], POINTER(c_int), 'pBufferSize'),
              (['out'], POINTER(c_int), 'pBuffer')),
    COMMETHOD([], HRESULT, 'GetCurrentSample',
              (['out', 'retval'], POINTER(POINTER(qedit.IMediaSample)), 'ppSample')),
    COMMETHOD([], HRESULT, 'SetCallback',
              ([], POINTER(qedit.ISampleGrabberCB), 'pCallback'),
              ([], c_int, 'WhichMethodToCallback'))]


class ICreateDevEnum(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{29840822-5B84-11D0-BD3B-00A0C911CE86}')
    _idlflags_ = []


ICreateDevEnum._methods_ = [
    COMMETHOD([], HRESULT, 'CreateClassEnumerator',
              (['in'], POINTER(GUID), 'clsidDeviceClass'),
              (['out'], POINTER(POINTER(IEnumMoniker)), 'ppEnumMoniker'),
              (['in'], c_int, 'dwFlags'))]


class IAMStreamConfig(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{c6e13340-30ac-11d0-a18c-00a0c9118956}')
    _idlflags_ = []


IAMStreamConfig._methods_ = [
    COMMETHOD([], HRESULT, 'SetFormat',
              (['in'], POINTER(qedit._AMMediaType), 'pmt')
              ),
    COMMETHOD([], HRESULT, 'GetFormat',
              (['out'], POINTER(POINTER(qedit._AMMediaType)), 'pmt')
              ),
    COMMETHOD([], HRESULT, 'GetNumberOfCapabilities',
              (['out'], POINTER(c_int), 'piCount'),
              (['out'], POINTER(c_int), 'piSize')
              ),
    COMMETHOD([], HRESULT, 'GetStreamCaps', #https://docs.microsoft.com/en-us/previous-versions/ms784114(v%3Dvs.85)
              (['in'], c_int, 'iIndex'),
              (['out'], POINTER(POINTER(qedit._AMMediaType)), 'pmt'),
              (['out'], POINTER(VIDEO_STREAM_CONFIG_CAPS), 'pSCC'))]


class ISpecifyPropertyPages(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{B196B28B-BAB4-101A-B69C-00AA00341D07}')
    _idlflags_ = []


class CAUUID(Structure):
    _fields_ = (
        ('element_count', ULONG),
        ('elements', POINTER(GUID)),
    )


ISpecifyPropertyPages._methods_ = [
    COMMETHOD([], HRESULT, 'GetPages',
              (['out'], POINTER(CAUUID), 'pPages'),
              )]


class IVideoWindow(IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{56a868b4-0ad4-11ce-b03a-0020af0ba770}')
    _idlflags_ = []


IVideoWindow._methods_ = [
    COMMETHOD([], HRESULT, 'put_Caption',
              (['in'], BSTR, 'strCaption')),

    COMMETHOD([], HRESULT, 'get_Caption',
              (['retval', 'out'], POINTER(BSTR), 'strCaption')),

    COMMETHOD([], HRESULT, 'put_WindowStyle',
              (['in'], c_long, 'WindowStyle')),

    COMMETHOD([], HRESULT, 'get_WindowStyle',
              (['retval', 'out'], POINTER(c_long), 'WindowStyle')),

    COMMETHOD([], HRESULT, 'put_WindowStyleEx',
              (['in'], c_long, 'WindowStyleEx')),

    COMMETHOD([], HRESULT, 'get_WindowStyleEx',
              (['retval', 'out'], POINTER(c_long), 'WindowStyleEx')),

    COMMETHOD([], HRESULT, 'put_AutoShow',
              (['in'], c_long, 'AutoShow')),

    COMMETHOD([], HRESULT, 'get_AutoShow',
              (['retval', 'out'], POINTER(c_long), 'AutoShow')),

    COMMETHOD([], HRESULT, 'put_WindowState',
              (['in'], c_long, 'WindowState')),

    COMMETHOD([], HRESULT, 'get_WindowState',
              (['retval', 'out'], POINTER(c_long), 'WindowState')),

    COMMETHOD([], HRESULT, 'put_BackgroundPalette',
              (['in'], c_long, 'BackgroundPalette')),

    COMMETHOD([], HRESULT, 'get_BackgroundPalette',
              (['retval', 'out'], POINTER(c_long), 'pBackgroundPalette')),

    COMMETHOD([], HRESULT, 'put_Visible',
              (['in'], c_long, 'Visible')),

    COMMETHOD([], HRESULT, 'get_Visible',
              (['retval', 'out'], POINTER(c_long), 'pVisible')),

    COMMETHOD([], HRESULT, 'put_Left',
              (['in'], c_long, 'Left')),

    COMMETHOD([], HRESULT, 'get_Left',
              (['retval', 'out'], POINTER(c_long), 'pLeft')),

    COMMETHOD([], HRESULT, 'put_Width',
              (['in'], c_long, 'Width')),

    COMMETHOD([], HRESULT, 'get_Width',
              (['retval', 'out'], POINTER(c_long), 'pWidth')),

    COMMETHOD([], HRESULT, 'put_Top',
              (['in'], c_long, 'Top')),

    COMMETHOD([], HRESULT, 'get_Top',
              (['retval', 'out'], POINTER(c_long), 'pTop')),

    COMMETHOD([], HRESULT, 'put_Height',
              (['in'], c_long, 'Height')),

    COMMETHOD([], HRESULT, 'get_Height',
              (['retval', 'out'], POINTER(c_long), 'pHeight')),

    COMMETHOD([], HRESULT, 'put_Owner',
              (['in'], OLE_HANDLE, 'Owner')),

    COMMETHOD([], HRESULT, 'get_Owner',
              (['retval', 'out'], POINTER(OLE_HANDLE), 'Owner')),

    COMMETHOD([], HRESULT, 'put_MessageDrain',
              (['in'], OLE_HANDLE, 'Drain')),

    COMMETHOD([], HRESULT, 'get_MessageDrain',
              (['retval', 'out'], POINTER(OLE_HANDLE), 'Drain')),

    COMMETHOD([], HRESULT, 'get_BorderColor',
              (['retval', 'out'], POINTER(c_long), 'Color')),

    COMMETHOD([], HRESULT, 'put_BorderColor',
              (['in'], c_long, 'Color')),

    COMMETHOD([], HRESULT, 'get_FullScreenMode',
              (['retval', 'out'], POINTER(c_long), 'FullScreenMode')),

    COMMETHOD([], HRESULT, 'put_FullScreenMode',
              (['in'], c_long, 'FullScreenMode')),

    COMMETHOD([], HRESULT, 'SetWindowForeground',
              (['in'], c_long, 'Focus')),

    COMMETHOD([], HRESULT, 'NotifyOwnerMessage',
              (['in'], OLE_HANDLE, 'hwnd'),
              (['in'], c_long, 'uMsg'),
              (['in'], LONG_PTR, 'wParam'),
              (['in'], LONG_PTR, 'lParam')),

    COMMETHOD([], HRESULT, 'SetWindowPosition',
              (['in'], c_long, 'Left'),
              (['in'], c_long, 'Top'),
              (['in'], c_long, 'Width'),
              (['in'], c_long, 'Height')),

    COMMETHOD([], HRESULT, 'GetWindowPosition',
              (['out'], POINTER(c_long), 'pLeft'),
              (['out'], POINTER(c_long), 'pTop'),
              (['out'], POINTER(c_long), 'pWidth'),
              (['out'], POINTER(c_long), 'pHeight')),

    COMMETHOD([], HRESULT, 'GetMinIdealImageSize',
              (['out'], POINTER(c_long), 'pWidth'),
              (['out'], POINTER(c_long), 'pHeight')),

    COMMETHOD([], HRESULT, 'GetMaxIdealImageSize',
              (['out'], POINTER(c_long), 'pWidth'),
              (['out'], POINTER(c_long), 'pHeight')),

    COMMETHOD([], HRESULT, 'GetRestorePosition',
              (['out'], POINTER(c_long), 'pLeft'),
              (['out'], POINTER(c_long), 'pTop'),
              (['out'], POINTER(c_long), 'pWidth'),
              (['out'], POINTER(c_long), 'pHeight')),

    COMMETHOD([], HRESULT, 'HideCursor',
              (['in'], c_long, 'HideCursor')),

    COMMETHOD([], HRESULT, 'IsCursorHidden',
              (['out'], POINTER(c_long), 'CursorHidden'))
]


class ICaptureGraphBuilder2(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{93E5A4E0-2D50-11d2-ABFA-00A0C9C6E38D}')
    _idlflags_ = []


ICaptureGraphBuilder2._methods_ = [
    COMMETHOD([], HRESULT, 'SetFiltergraph',
              (['in'], POINTER(qedit.IFilterGraph), 'pfg')),

    COMMETHOD([], HRESULT, 'GetFiltergraph',
              (['out'], POINTER(POINTER(qedit.IFilterGraph)), 'pfg')),

    COMMETHOD([], HRESULT, 'SetOutputFileName',
              (['in'], POINTER(GUID), 'pType'),
              (['in'], LPCOLESTR, 'lpstrFile'),
              (['out'], POINTER(POINTER(qedit.IBaseFilter)), 'ppf'),
              (['out'], POINTER(POINTER(qedit.IBaseFilter)), 'pSink')),

    COMMETHOD([], HRESULT, 'FindInterface',
              (['in'], POINTER(GUID), 'pCategory'),
              (['in'], POINTER(GUID), 'pType'),
              (['in'], POINTER(qedit.IBaseFilter), 'pf'),
              (['in'], REFIID, 'REFIID'),
              (['out'], POINTER(POINTER(None)), 'ppINT')),

    COMMETHOD([], HRESULT, 'RenderStream',
              (['in'], POINTER(GUID), 'pCategory'),
              (['in'], POINTER(GUID), 'pType'),
              (['in'], POINTER(qedit.IBaseFilter), 'pSource'),
              (['in'], POINTER(qedit.IBaseFilter), 'pIntermediate'),
              (['in'], POINTER(qedit.IBaseFilter), 'pSink')),

    COMMETHOD([], HRESULT, 'ControlStream',
              (['in'], POINTER(GUID), 'pCategory'),
              (['in'], POINTER(GUID), 'pType'),
              (['in'], POINTER(qedit.IBaseFilter), 'pFilter'),
              (['in'], POINTER(REFERENCE_TIME), 'pstart'),
              (['in'], POINTER(REFERENCE_TIME), 'pstop'),
              (['in'], WORD, 'wStartCookie'),
              (['in'], WORD, 'wStopCookie')),

    COMMETHOD([], HRESULT, 'AllocCapFile',
              (['in'], LPCOLESTR, 'lpstr'),
              (['in'], DWORDLONG, 'dwlSize')),

    COMMETHOD([], HRESULT, 'CopyCaptureFile',
              (['in'], LPOLESTR, 'lpwstrOld'),
              (['in'], LPOLESTR, 'lpwstrNew'),
              (['in'], c_int, 'fAllowEscAbort'),
              (['in'], POINTER(IUnknown), 'pCallback')),
    # (['in'], POINTER(IAMCopyCaptureFileProgress), 'pCallback'),

    COMMETHOD([], HRESULT, 'FindPin',
              (['in'], POINTER(qedit.IBaseFilter), 'pSource'),
              (['in'], c_int, 'pindir'),
              (['in'], POINTER(GUID), 'pCategory'),
              (['in'], POINTER(GUID), 'pType'),
              (['in'], c_int, 'fUnconnected'),
              (['in'], c_int, 'num'),
              (['out'], POINTER(POINTER(qedit.IPin)), 'ppPin'))
]
