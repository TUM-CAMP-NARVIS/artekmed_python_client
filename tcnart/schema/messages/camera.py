from dataclasses import dataclass, field
from enum import IntEnum

from ..types.transform import RigidTransform
from ..types.primitives import CameraModel
from ...serialization.cdr_serialization import register_type
from pycdr2 import IdlStruct, IdlEnum
from pycdr2.types import int32, uint32, float64, float32, sequence, uint8, uint16, uint64, array


class CameraSensorTypesEnum(IdlEnum, typename="CameraSensorTypesEnum"):
    GenericRgbd = 0
    KinectAzure = 1
    FemtoMega = 2


@dataclass
class CameraSensorMessage(IdlStruct, typename="CameraSensorMessage"):
    name: str = ""
    serial_number: str = ""
    camera_type: CameraSensorTypesEnum = CameraSensorTypesEnum.GenericRgbd
    depth_enabled: bool = False
    color_enabled: bool = False
    infrared_enabled: bool = False
    depth_descriptor_topic: str = ""
    infrared_descriptor_topic: str = ""
    depth_parameters: CameraModel = field(default_factory=CameraModel)
    color_descriptor_topic: str = ""
    color_parameters: CameraModel = field(default_factory=CameraModel)
    camera_pose: RigidTransform = field(default_factory=RigidTransform)
    color2depth_transform: RigidTransform = field(default_factory=RigidTransform)
    frame_rate: uint32 = 0
    raw_calibration: sequence[uint8] = field(default_factory=list)
    depth_units_per_meter: float32 = 1.0
    timestamp_offset_ns: uint64 = 0


# Register schema name
register_type("pcpd_msgs::msg::CameraSensor", CameraSensorMessage)
