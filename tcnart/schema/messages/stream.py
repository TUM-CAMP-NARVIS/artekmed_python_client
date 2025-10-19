from dataclasses import dataclass, field

from ..types.common import Header, MarkerType, BufferInfo, SensorType
from ..types.transform import RigidTransform
from ..types.format import (
    VideoPixelFormat,
    VideoImageCompression,
    VideoH26xProfile,
    AudioAACProfile,
)
from ..types.primitives import CameraModel
from ...serialization.cdr_serialization import register_type
from pycdr2 import IdlStruct
from pycdr2.types import int32, uint32, float64, float32, sequence, uint8, uint16, uint64, array


@dataclass
class CameraInfoMessage(IdlStruct, typename="CameraInfoMessage"):
    header: Header = field(default_factory=Header)
    value: CameraModel = field(default_factory=CameraModel)

    def get_timestamp(self) -> int:
        return self.header.stamp.to_timestamp()


@dataclass
class StreamDescriptorMessage(IdlStruct, typename="StreamDescriptorMessage"):
    header: Header = field(default_factory=Header)
    stream_topic: str = ""
    stream_topic_schema: str = ""
    calib_topic: str = ""
    calib_topic_schema: str = ""
    sensor_type: SensorType = SensorType.SensorTypeNone
    frame_rate: uint32 = 0
    buffer_info: BufferInfo = field(default_factory=BufferInfo)
    pose: RigidTransform = field(default_factory=RigidTransform)
    marker_type: MarkerType = MarkerType.MarkerTypeNone
    image_height: uint32 = 0
    image_width: uint32 = 0
    image_step: uint32 = 0
    image_format: VideoPixelFormat = VideoPixelFormat.PixelFormatNV12
    image_compression: VideoImageCompression = VideoImageCompression.CompressionTypeRaw
    h26x_profile: VideoH26xProfile = VideoH26xProfile.H264ProfileBase
    h26x_bitrate: uint32 = 0
    audio_channels: uint8 = 0
    aac_profile: AudioAACProfile = AudioAACProfile.AACProfile12000

    def get_timestamp(self) -> int:
        return self.header.stamp.to_timestamp()


# Register schema type name mapping
register_type("tcnart_msgs::msg::StreamDescriptorMessage", StreamDescriptorMessage)
