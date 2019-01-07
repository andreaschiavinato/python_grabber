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

from ctypes import POINTER, HRESULT
from ctypes import windll
from ctypes.wintypes import (DWORD, ULONG, HWND,
                             UINT, LPCOLESTR, LCID, LPVOID)

from comtypes import IUnknown, GUID

LPUNKNOWN = POINTER(IUnknown)
CLSID = GUID
LPCLSID = POINTER(CLSID)

WS_CHILD = 0x40000000
WS_CLIPSIBLINGS = 0x04000000

OleCreatePropertyFrame = windll.oleaut32.OleCreatePropertyFrame
OleCreatePropertyFrame.restype = HRESULT
OleCreatePropertyFrame.argtypes = (
    HWND,  # [in] hwndOwner
    UINT,  # [in] x
    UINT,  # [in] y
    LPCOLESTR,  # [in] lpszCaption
    ULONG,  # [in] cObjects
    POINTER(LPUNKNOWN),  # [in] ppUnk
    ULONG,  # [in] cPages
    LPCLSID,  # [in] pPageClsID
    LCID,  # [in] lcid
    DWORD,  # [in] dwReserved
    LPVOID,  # [in] pvReserved
)
