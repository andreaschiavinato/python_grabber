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

from pygrabber.win_common_types import *
from comtypes import DWORD
from ctypes.wintypes import BOOL


LPCWSTR_WMSDK_TYPE_SAFE = POINTER(c_wchar)


class IWMStreamList(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{96406Bdd-2b2b-11d3-b36b-00c04f6108ff}')
    _idlflags_ = []


IWMStreamList._methods_ = [
    COMMETHOD([], HRESULT, 'GetStreams',
              (['in'], POINTER(DWORD), 'pwStreamNumArray'),
              (['in'], POINTER(DWORD), 'pcStreams')),

    COMMETHOD([], HRESULT, 'AddStream',
              (['in'], DWORD, 'wStreamNum')),

    COMMETHOD([], HRESULT, 'RemoveStream',
              (['in'], DWORD, 'wStreamNum'))]


class IWMMutualExclusion(IWMStreamList):
    _case_insensitive_ = True
    _iid_ = GUID('{96406Bde-2b2b-11d3-b36b-00c04f6108ff}')
    _idlflags_ = []


IWMMutualExclusion._methods_ = [
    COMMETHOD([], HRESULT, 'GetType',
              (['out'], POINTER(GUID), 'pguidType')),

    COMMETHOD([], HRESULT, 'SetType',
              (['in'], REFGUID, 'guidType'))]


class IWMStreamConfig(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{96406Bdc-2b2b-11d3-b36b-00c04f6108ff}')
    _idlflags_ = []


IWMStreamConfig._methods_ = [
    COMMETHOD([], HRESULT, 'GetStreamType',
              (['out'], POINTER(GUID), 'pguidStreamType')),

    COMMETHOD([], HRESULT, 'GetStreamNumber',
              (['out'], POINTER(WORD), 'pwStreamNum')),

    COMMETHOD([], HRESULT, 'SetStreamNumber',
              (['in'], WORD, 'wStreamNum')),

    COMMETHOD([], HRESULT, 'GetStreamName',
              (['in'], POINTER(c_wchar), 'pwszStreamName'),
              (['in'], POINTER(WORD), 'pcchStreamName')),

    COMMETHOD([], HRESULT, 'SetStreamName',
              (['in'], LPCWSTR_WMSDK_TYPE_SAFE, 'pwszStreamName')),

    COMMETHOD([], HRESULT, 'GetConnectionName',
              (['out'], POINTER(c_wchar), 'pwszInputName'),
              (['in'], POINTER(WORD), 'pcchInputName')),

    COMMETHOD([], HRESULT, 'SetConnectionName',
              (['in'], LPCWSTR_WMSDK_TYPE_SAFE, 'pwszInputName')),

    COMMETHOD([], HRESULT, 'GetBitrate',
              (['out'], POINTER(WORD), 'pdwBitrate')),

    COMMETHOD([], HRESULT, 'SetBitrate',
              (['in'], DWORD, 'pdwBitrate')),

    COMMETHOD([], HRESULT, 'pmsBufferWindow',
              (['out'], POINTER(WORD), 'pmsBufferWindow')),

    COMMETHOD([], HRESULT, 'SetBufferWindow',
              (['in'], DWORD, 'msBufferWindow'))]


class IWMProfile(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{96406BDB-2B2B-11D3-B36B-00C04F6108FF}')
    _idlflags_ = []


IWMProfile._methods_ = [
    COMMETHOD([], HRESULT, 'GetVersion',
              (['out'], POINTER(DWORD), 'pdwVersion')),

    COMMETHOD([], HRESULT, 'GetName',
              (['in'], POINTER(c_wchar), 'pwszName'),
              (['in'], POINTER(DWORD), 'pcchName')),

    COMMETHOD([], HRESULT, 'SetName',
              (['in'], POINTER(c_wchar), 'pwszName')),

    COMMETHOD([], HRESULT, 'GetDescription',
              (['in'], POINTER(c_wchar), 'pwszDescription'),
              (['in'], POINTER(DWORD), 'pcchDescription')),

    COMMETHOD([], HRESULT, 'SetDescription',
              (['in'], POINTER(c_wchar), 'pwszDescription')),

    COMMETHOD([], HRESULT, 'GetStreamCount',
              (['out'], POINTER(DWORD), 'pcStreams')),

    COMMETHOD([], HRESULT, 'GetStream',
              (['in'], DWORD, 'dwStreamIndex'),
              (['out'], POINTER(POINTER(IWMStreamConfig)), 'ppConfig')),

    COMMETHOD([], HRESULT, 'GetStreamByNumber',
              (['in'], DWORD, 'wStreamNum'),
              (['out'], POINTER(POINTER(IWMStreamConfig)), 'ppConfig')),

    COMMETHOD([], HRESULT, 'RemoveStream',
              (['in'], POINTER(IWMStreamConfig), 'pConfig')),

    COMMETHOD([], HRESULT, 'RemoveStreamByNumber',
              (['in'], DWORD, 'wStreamNum')),

    COMMETHOD([], HRESULT, 'AddStream',
              (['in'], POINTER(IWMStreamConfig), 'pConfig')),

    COMMETHOD([], HRESULT, 'ReconfigStream',
              (['in'], POINTER(IWMStreamConfig), 'pConfig')),

    COMMETHOD([], HRESULT, 'CreateNewStream',
              (['in'], REFGUID, 'guidStreamType'),
              (['out'], POINTER(POINTER(IWMStreamConfig)), 'ppConfig')),

    COMMETHOD([], HRESULT, 'GetMutualExclusionCount',
              (['out'], POINTER(DWORD), 'pcME')),

    COMMETHOD([], HRESULT, 'GetMutualExclusion',
              (['in'], DWORD, 'dwMEIndex'),
              (['out'], POINTER(POINTER(IWMMutualExclusion)), 'ppME')),

    COMMETHOD([], HRESULT, 'RemoveMutualExclusion',
              (['in'], POINTER(IWMMutualExclusion), 'pME')),

    COMMETHOD([], HRESULT, 'AddMutualExclusion',
              (['in'], POINTER(IWMMutualExclusion), 'pME')),

    COMMETHOD([], HRESULT, 'CreateNewMutualExclusion',
              (['out'], POINTER(POINTER(IWMMutualExclusion)), 'ppME'))
]


class IWMProfileManager2(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{d16679f2-6ca0-472d-8d31-2f5d55aee155}')
    _idlflags_ = []


IWMProfileManager2._methods_ = [
    COMMETHOD([], HRESULT, 'CreateEmptyProfile',
              (['in'], DWORD, 'dwVersion'),
              (['out'], POINTER(POINTER(IWMProfile)), 'ppProfile')),

    COMMETHOD([], HRESULT, 'LoadProfileByID',
              (['in'], REFGUID, 'guidProfile'),
              (['out'], POINTER(POINTER(IWMProfile)), 'ppProfile')),

    COMMETHOD([], HRESULT, 'LoadProfileByData',
              (['in'], c_wchar_p, 'pwszProfile'),
              (['out'], POINTER(POINTER(IWMProfile)), 'ppProfile')),

    COMMETHOD([], HRESULT, 'SaveProfile',
              (['in'], POINTER(IWMProfile), 'pIWMProfile'),
              (['in'], c_wchar_p, 'pwszProfile'),
              (['in'], POINTER(DWORD), 'pdwLength')),

    COMMETHOD([], HRESULT, 'GetSystemProfileCount',
              (['out'], POINTER(DWORD), 'pcProfiles')),

    COMMETHOD([], HRESULT, 'LoadSystemProfile',
              (['in'], DWORD, 'dwProfileIndex'),
              (['out'], POINTER(POINTER(IWMProfile)), 'ppProfile')),

    COMMETHOD([], HRESULT, 'GetSystemProfileVersion',
              (['out'], POINTER(DWORD), 'pdwVersion')),

    COMMETHOD([], HRESULT, 'SetSystemProfileVersion',
              (['in'], DWORD, 'dwVersion')),
]


WMCreateProfileManager = windll.Wmvcore.WMCreateProfileManager
WMCreateProfileManager.restype = HRESULT
WMCreateProfileManager.argtypes = [POINTER(POINTER(IWMProfileManager2))]


class IConfigAsfWriter(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{45086030-F7E4-486a-B504-826BB5792A3B}')
    _idlflags_ = []


IConfigAsfWriter._methods_ = [
    COMMETHOD([], HRESULT, 'ConfigureFilterUsingProfileId',
              (['in'], DWORD, 'dwProfileId')),

    COMMETHOD([], HRESULT, 'GetCurrentProfileId',
              (['out'], POINTER(DWORD), 'pdwProfileId')),

    COMMETHOD([], HRESULT, 'ConfigureFilterUsingProfileGuid',
              (['in'], REFGUID, 'guidProfile')),

    COMMETHOD([], HRESULT, 'GetCurrentProfileGuid',
              (['out'], POINTER(GUID), 'pProfileGuid')),

    COMMETHOD([], HRESULT, 'ConfigureFilterUsingProfile',
              (['in'], POINTER(IWMProfile), 'pProfile')),

    COMMETHOD([], HRESULT, 'GetCurrentProfile',
              (['out'], POINTER(POINTER(IWMProfile)), 'ppProfile')),

    COMMETHOD([], HRESULT, 'SetIndexMode',
              (['in'], BOOL, 'bIndexFile')),

    COMMETHOD([], HRESULT, 'GetIndexMode',
              (['out'], POINTER(BOOL), 'pbIndexFile'))]
