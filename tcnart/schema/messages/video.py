from dataclasses import dataclass, field
from typing import List

from ..types.common import Header
from ..types.transform import RigidTransform
from ...serialization.cdr_serialization import register_type
from pycdr2 import IdlStruct
from pycdr2.types import int32, uint32, float64, float32, sequence, uint8, uint16, uint64, array


@dataclass
class VideoStreamMessage(IdlStruct, typename="VideoStreamMessage"):
    header: Header = field(default_factory=Header)
    pose: RigidTransform = field(default_factory=RigidTransform)
    camera_focal_length: array[float32, 2] = (1.0, 1.0)
    camera_principal_point: array[float32, 2] = (0.0, 0.0)
    camera_radial_distortion: array[float32, 3] = (0.0, 0.0, 0.0)
    camera_tangential_distortion: array[float32, 2] = (0.0, 0.0)
    image_bytes: uint64 = 0
    image: sequence[uint8] = field(default_factory=list)

    @staticmethod
    def new() -> "VideoStreamMessage":
        return VideoStreamMessage()

    def get_timestamp(self) -> int:
        return self.header.stamp.to_timestamp()


# Register schema type name mapping to enable decode_raw_message()
register_type("tcnart_msgs::msg::VideoStreamMessage", VideoStreamMessage)
