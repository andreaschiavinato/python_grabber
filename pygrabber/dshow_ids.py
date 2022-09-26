#
# python_grabber
#
# Authors:
#  Andrea Schiavinato <andrea.schiavinato84@gmail.com>
#
# Copyright (C) 2019 Andrea Schiavinato
#
# Permission is hereby grantedfree of chargeto any person obtaining
# a copy of this software and associated documentation files (the
# "Software")to deal in the Software without restrictionincluding
# without limitation the rights to usecopymodifymergepublish,
# distributesublicenseand/or sell copies of the Softwareand to
# permit persons to whom the Software is furnished to do sosubject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS"WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIEDINCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITYFITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIMDAMAGES OR OTHER LIABILITYWHETHER IN AN ACTION
# OF CONTRACTTORT OR OTHERWISEARISING FROMOUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from comtypes import GUID

GUID_NULL = GUID('{00000000-0000-0000-0000-000000000000}')


class clsids:
    CLSID_FilterGraph = '{E436EBB3-524F-11CE-9F53-0020AF0BA770}'
    CLSID_SystemDeviceEnum = '{62BE5D10-60EB-11d0-BD3B-00A0C911CE86}'
    CLSID_SampleGrabber = '{C1F400A0-3F08-11d3-9F0B-006008039E37}'
    CLSID_CaptureGraphBuilder2 = '{BF87B6E1-8C27-11d0-B3F0-00AA003761C5}'
    CLSID_VideoRendererDefault = '{6BC1CFFA-8FC1-4261-AC22-CFB4CC38DB50}'
    CLSID_NullRender = '{C1F400A4-3F08-11D3-9F0B-006008039E37}'
    CLSID_VideoMixingRenderer = '{B87BEB7B-8D29-423f-AE4D-6582C10175AC}'
    CLSID_SmartTee = '{CC58E280-8AA1-11d1-B3F1-00AA003761C5}'


class FormatTypes:
    FORMAT_None = '{0F6417D6-C318-11D0-A43F-00A0C9223196}'
    FORMAT_VideoInfo = '{05589f80-c356-11ce-bf01-00aa0055595a}'
    FORMAT_VideoInfo2 = '{F72A76A0-EB0A-11d0-ACE4-0000C0CC16BA}'
    FORMAT_WaveFormatEx = '{05589f81-c356-11ce-bf01-00aa0055595a}'
    FORMAT_MPEGVideo = '{05589f82-c356-11ce-bf01-00aa0055595a}'
    FORMAT_MPEGStreams = '{05589f83-c356-11ce-bf01-00aa0055595a}'
    FORMAT_DvInfo = '{05589f84-c356-11ce-bf01-00aa0055595a}'
    FORMAT_525WSS = '{C7ECF04D-4582-4869-9ABB-BFB523B62EDF}'


class DeviceCategories:
    VideoInputDevice = '{860bb310-5d01-11d0-bd3b-00a0c911ce86}'
    AudioInputDevice = '{33d9a762-90c8-11d0-bd43-00a0c911ce86}'
    VideoCompressor = '{33d9a760-90c8-11d0-bd43-00a0c911ce86}'
    AudioCompressor = '{33d9a761-90c8-11d0-bd43-00a0c911ce86}'
    LegacyAmFilter = '{083863F1-70DE-11d0-BD40-00A0C911CE86}'


class MediaTypes:
    Video = '{73646976-0000-0010-8000-00AA00389B71}'
    Audio = '{73647561-0000-0010-8000-00AA00389B71}'


class MediaSubtypes:
    RGB24 = '{E436EB7D-524F-11CE-9F53-0020AF0BA770}'
    AVI = '{E436EB88-524F-11CE-9F53-0020AF0BA770}'
    ASF = '{3DB80F90-9412-11D1-ADED-0000F8754B99}'


class PinCategory:
    Preview = '{fb6c4282-0353-11d1-905f-0000c0cc16ba}'
    Capture = '{fb6c4281-0353-11d1-905f-0000c0cc16ba}'


subtypes = {
    '{4C504C43-0000-0010-8000-00AA00389B71}': 'CLPL',
    '{56595559-0000-0010-8000-00AA00389B71}': 'YUYV',
    '{56555949-0000-0010-8000-00AA00389B71}': 'IYUV',
    '{39555659-0000-0010-8000-00AA00389B71}': 'YVU9',
    '{31313459-0000-0010-8000-00AA00389B71}': 'Y411',
    '{50313459-0000-0010-8000-00AA00389B71}': 'Y41P',
    '{32595559-0000-0010-8000-00AA00389B71}': 'YUY2',
    '{55595659-0000-0010-8000-00AA00389B71}': 'YVYU',
    '{59565955-0000-0010-8000-00AA00389B71}': 'UYVY',
    '{31313259-0000-0010-8000-00AA00389B71}': 'Y211',
    '{524A4C43-0000-0010-8000-00AA00389B71}': 'CLJR',
    '{39304649-0000-0010-8000-00AA00389B71}': 'IF09',
    '{414C5043-0000-0010-8000-00AA00389B71}': 'CPLA',
    '{47504A4D-0000-0010-8000-00AA00389B71}': 'MJPG',
    '{4A4D5654-0000-0010-8000-00AA00389B71}': 'TVMJ',
    '{454B4157-0000-0010-8000-00AA00389B71}': 'WAKE',
    '{43434643-0000-0010-8000-00AA00389B71}': 'CFCC',
    '{47504A49-0000-0010-8000-00AA00389B71}': 'IJPG',
    '{6D756C50-0000-0010-8000-00AA00389B71}': 'PLUM',
    '{53435644-0000-0010-8000-00AA00389B71}': 'DVCS',
    '{34363248-0000-0010-8000-00AA00389B71}': 'H264',
    '{44535644-0000-0010-8000-00AA00389B71}': 'DVSD',
    '{4656444D-0000-0010-8000-00AA00389B71}': 'MDVF',
    '{E436EB78-524F-11CE-9F53-0020AF0BA770}': 'RGB1',
    '{E436EB78-524F-11CE-9F53-0020AF0BA770}': 'RGB1',
    '{E436EB79-524F-11CE-9F53-0020AF0BA770}': 'RGB4',
    '{E436EB7A-524F-11CE-9F53-0020AF0BA770}': 'RGB8',
    '{E436EB7B-524F-11CE-9F53-0020AF0BA770}': 'RGB565',
    '{E436EB7C-524F-11CE-9F53-0020AF0BA770}': 'RGB555',
    '{E436EB7D-524F-11CE-9F53-0020AF0BA770}': 'RGB24',
    '{E436EB7E-524F-11CE-9F53-0020AF0BA770}': 'RGB32',
    '{297C55AF-E209-4CB3-B757-C76D6B9C88A8}': 'ARGB1555',
    '{6E6415E6-5C24-425F-93CD-80102B3D1CCA}': 'ARGB4444',
    '{773C9AC0-3274-11D0-B724-00AA006C1A01}': 'ARGB32',
    '{2F8BB76D-B644-4550-ACF3-D30CAA65D5C5}': 'A2R10G10B10',
    '{576F7893-BDF6-48C4-875F-AE7B81834567}': 'A2B10G10R10',
    '{56555941-0000-0010-8000-00AA00389B71}': 'AYUV',
    '{34344941-0000-0010-8000-00AA00389B71}': 'AI44',
    '{34344149-0000-0010-8000-00AA00389B71}': 'IA44',
    '{32335237-0000-0010-8000-00AA00389B71}': 'RGB32_D3D_DX7_RT',
    '{36315237-0000-0010-8000-00AA00389B71}': 'RGB16_D3D_DX7_RT',
    '{38384137-0000-0010-8000-00AA00389B71}': 'ARGB32_D3D_DX7_RT',
    '{34344137-0000-0010-8000-00AA00389B71}': 'ARGB4444_D3D_DX7_RT',
    '{35314137-0000-0010-8000-00AA00389B71}': 'ARGB1555_D3D_DX7_RT',
    '{32335239-0000-0010-8000-00AA00389B71}': 'RGB32_D3D_DX9_RT',
    '{36315239-0000-0010-8000-00AA00389B71}': 'RGB16_D3D_DX9_RT',
    '{38384139-0000-0010-8000-00AA00389B71}': 'ARGB32_D3D_DX9_RT',
    '{34344139-0000-0010-8000-00AA00389B71}': 'ARGB4444_D3D_DX9_RT',
    '{35314139-0000-0010-8000-00AA00389B71}': 'ARGB1555_D3D_DX9_RT',
    '{32315659-0000-0010-8000-00AA00389B71}': 'YV12',
    '{3231564E-0000-0010-8000-00AA00389B71}': 'NV12',
    '{3131564E-0000-0010-8000-00AA00389B71}': 'NV11',
    '{38303250-0000-0010-8000-00AA00389B71}': 'P208',
    '{30313250-0000-0010-8000-00AA00389B71}': 'P210',
    '{36313250-0000-0010-8000-00AA00389B71}': 'P216',
    '{30313050-0000-0010-8000-00AA00389B71}': 'P010',
    '{36313050-0000-0010-8000-00AA00389B71}': 'P016',
    '{30313259-0000-0010-8000-00AA00389B71}': 'Y210',
    '{36313259-0000-0010-8000-00AA00389B71}': 'Y216',
    '{38303450-0000-0010-8000-00AA00389B71}': 'P408',
    '{3432564E-0000-0010-8000-00AA00389B71}': 'NV24',
    '{4F303234-0000-0010-8000-00AA00389B71}': '420O',
    '{31434D49-0000-0010-8000-00AA00389B71}': 'IMC1',
    '{32434D49-0000-0010-8000-00AA00389B71}': 'IMC2',
    '{33434D49-0000-0010-8000-00AA00389B71}': 'IMC3',
    '{34434D49-0000-0010-8000-00AA00389B71}': 'IMC4',
    '{30343353-0000-0010-8000-00AA00389B71}': 'S340',
    '{32343353-0000-0010-8000-00AA00389B71}': 'S342',
    '{E436EB7F-524F-11CE-9F53-0020AF0BA770}': 'OVERLAY',
    '{E436EB80-524F-11CE-9F53-0020AF0BA770}': 'MPEGPACKET',
    '{E436EB81-524F-11CE-9F53-0020AF0BA770}': 'MPEG1PAYLOAD',
    '{00000050-0000-0010-8000-00AA00389B71}': 'MPEG1AUDIOPAYLOAD',
    '{E436EB82-524F-11CE-9F53-0020AF0BA770}': 'MPEG1SYSTEMSTREAM',
    '{E436EB84-524F-11CE-9F53-0020AF0BA770}': 'MPEG1SYSTEM',
    '{E436EB85-524F-11CE-9F53-0020AF0BA770}': 'MPEG1VIDEOCD',
    '{E436EB86-524F-11CE-9F53-0020AF0BA770}': 'MPEG1VIDEO',
    '{E436EB87-524F-11CE-9F53-0020AF0BA770}': 'MPEG1AUDIO',
    '{E436EB88-524F-11CE-9F53-0020AF0BA770}': 'AVI',
    '{3DB80F90-9412-11D1-ADED-0000F8754B99}': 'ASF',
    '{E436EB89-524F-11CE-9F53-0020AF0BA770}': 'QTMOVIE',
    '{617A7072-0000-0010-8000-00AA00389B71}': 'RPZA',
    '{20636D73-0000-0010-8000-00AA00389B71}': 'SMC',
    '{20656C72-0000-0010-8000-00AA00389B71}': 'RLE',
    '{6765706A-0000-0010-8000-00AA00389B71}': 'JPEG',
    '{E436EB8A-524F-11CE-9F53-0020AF0BA770}': 'PCMAUDIO_OBSOLETE',
    '{00000001-0000-0010-8000-00AA00389B71}': 'PCM',
    '{E436EB8B-524F-11CE-9F53-0020AF0BA770}': 'WAVE',
    '{E436EB8C-524F-11CE-9F53-0020AF0BA770}': 'AU',
    '{E436EB8D-524F-11CE-9F53-0020AF0BA770}': 'AIFF',
    '{6E8D4A22-310C-11D0-B79A-00AA003767A7}': 'LINE21_BYTEPAIR',
    '{6E8D4A23-310C-11D0-B79A-00AA003767A7}': 'LINE21_GOPPACKET',
    '{6E8D4A24-310C-11D0-B79A-00AA003767A7}': 'LINE21_VBIRAWDATA',
    '{0AF414BC-4ED2-445E-9839-8F095568AB3C}': '708_608DATA',
    '{F52ADDAA-36F0-43F5-95EA-6D866484262A}': 'DTVCCDATA',
    '{7EA626DB-54DA-437B-BE9F-F73073ADFA3C}': 'CC_CONTAINER',
    '{F72A76E3-EB0A-11D0-ACE4-0000C0CC16BA}': 'TELETEXT',
    '{663DA43C-03E8-4E9A-9CD5-BF11ED0DEF76}': 'VBI',
    '{2791D576-8E7A-466F-9E90-5D3F3083738B}': 'WSS',
    '{01CA73E3-DCE6-4575-AFE1-2BF1C902CAF3}': 'XDS',
    '{A1B3F620-9792-4D8D-81A4-86AF25772090}': 'VPS'
}
