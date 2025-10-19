from dataclasses import dataclass, field
from enum import IntEnum
from pycdr2 import IdlStruct
from pycdr2.types import int32, uint32, float64, float32, sequence, uint8, uint16, uint64, array

from ..types.common import BufferInfo
from .camera import CameraSensorMessage
from .rpc import RPCResponseStatus, ParameterListSchema
from ...serialization.cdr_serialization import register_type


class ServiceType(IntEnum):
    StCore = 0
    StProducer = 1
    StConsumer = 2


class RecorderStatus(IntEnum):
    RsInvalid = 0
    RsIdle = 1
    RsRecording = 2
    RsPaused = 3
    RsError = 4


@dataclass
class DeviceContextReply(IdlStruct, typename="DeviceContextReply"):
    name: str = ""
    is_valid: bool = False
    depth_units_per_meter: float32 = 1.0
    frame_rate: int32 = 0
    sensor_type: str = ""
    serial_number: str = ""
    timestamp_offset: uint64 = 0
    value: CameraSensorMessage = field(default_factory=CameraSensorMessage)
    status: RPCResponseStatus = RPCResponseStatus.RpcStatusSuccess


@dataclass
class BufferInfoReply(IdlStruct, typename="BufferInfoReply"):
    value: BufferInfo = field(default_factory=BufferInfo)
    status: RPCResponseStatus = RPCResponseStatus.RpcStatusSuccess


@dataclass
class ServiceInfoReply(IdlStruct, typename="ServiceInfoReply"):
    name: str = ""
    service_type: str = ""
    schema: ParameterListSchema = field(default_factory=ParameterListSchema)
    status: RPCResponseStatus = RPCResponseStatus.RpcStatusSuccess


@dataclass
class ComponentInfoReply(IdlStruct, typename="ComponentInfoReply"):
    name: str = ""
    component_type: str = ""
    schema: ParameterListSchema = field(default_factory=ParameterListSchema)
    status: RPCResponseStatus = RPCResponseStatus.RpcStatusSuccess


# Register schema mapping used by Rust decoder mapping
register_type("pcpd_msgs::rpc::DeviceContextReply", DeviceContextReply)
