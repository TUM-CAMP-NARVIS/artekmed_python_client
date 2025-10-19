from pycdr2 import IdlStruct, IdlEnum
from pycdr2.types import int32, uint32, float64, float32, sequence, uint8, uint16, uint64, array


class VideoPixelFormat(IdlEnum, typename="VideoPixelFormat"):
    PixelFormatNV12 = 0
    PixelFormatRGB24 = 1
    PixelFormatBGR24 = 2
    PixelFormatBGRA32 = 3
    PixelFormatL8 = 4
    PixelFormatL16 = 5


class VideoImageCompression(IdlEnum, typename="VideoImageCompression"):
    CompressionTypeRaw = 0
    CompressionTypePng = 1
    CompressionTypeH26x = 2
    CompressionTypeZdepth = 3
    CompressionTypeJpeg = 4


class VideoH26xProfile(IdlEnum, typename="VideoH26xProfile"):
    H264ProfileBase = 0
    H264ProfileMain = 1
    H264ProfileHigh = 2
    H265ProfileMain = 3
    H26xProfileNone = 4


class AudioAACProfile(IdlEnum, typename="AudioAACProfile"):
    AACProfile12000 = 0
    AACProfile16000 = 1
    AACProfile20000 = 2
    AACProfile24000 = 3
    AACProfileNone = 4
