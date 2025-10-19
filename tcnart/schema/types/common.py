from dataclasses import dataclass, field
from typing import List, Tuple
from pycdr2 import IdlStruct, IdlEnum
from pycdr2.types import int32, uint32, float64, float32, sequence, uint8, uint16, uint64, array

class SensorType(IdlEnum, typename="SensorType"):
    SensorTypeNone = 0
    SensorTypeVideoColor = 1
    SensorTypeVideoDepth = 2
    SensorTypeVideoIr = 3
    SensorTypeTrackingPose = 4
    SensorTypeTrackingEye = 5
    SensorTypeTrackingHand = 6
    SensorTypeTrackingBody = 7
    SensorTypeAudio = 8
    SensorTypeImuAccel = 9
    SensorTypeImuGyro = 10
    SensorTypeImuMag = 11
    SensorTypeMeshBitstream = 12
    SensorTypeSurfel = 13


class CameraModelType(IdlEnum, typename="CameraModelType"):
    CameraModelNone = 0
    CameraModelPinhole = 1
    CameraModelOpenCv = 2
    CameraModelFullOpenCv = 3
    CameraModelSensorAzureKinect = 4


class MarkerType(IdlEnum, typename="MarkerType"):
    MarkerTypeNone = 0
    MarkerTypeArucoMarker = 1
    MarkerTypeArucoBoard = 2
    MarkerTypeArucoFractal = 3
    MarkerTypeIrTarget = 4


@dataclass
class MSGuid(IdlStruct, typename="MSGuid"):
    data1: uint32 = 0
    data2: uint16 = 0
    data3: uint16 = 0
    data4: array[uint8, 8] = (0, 0, 0, 0, 0, 0, 0, 0)


@dataclass
class UUID(IdlStruct, typename="UUID"):
    uuid: array[uint8, 16] = (
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    )


@dataclass
class Time(IdlStruct, typename="Time"):
    sec: int32 = 0
    nanosec: uint32 = 0

    def to_timestamp(self) -> int:
        return int32(self.sec) * 1_000_000_000 + uint32(self.nanosec)


@dataclass
class Duration(IdlStruct, typename="Duration"):
    sec: int32 = 0
    nanosec: uint32 = 0


@dataclass
class Header(IdlStruct, typename="Header"):
    stamp: Time = field(default_factory=Time)
    frame_id: str = ""


@dataclass
class BufferInfoPropertyUserData(IdlStruct, typename="BufferInfoPropertyUserData"):
    key: str = ""
    value: sequence[uint8] = field(default_factory=list)


@dataclass
class BufferInfoProperty(IdlStruct, typename="BufferInfoProperty"):
    name: str = ""
    value: int32 = 0
    user_data: sequence[BufferInfoPropertyUserData] = field(default_factory=list)


@dataclass
class BufferInfo(IdlStruct, typename="BufferInfo"):
    is_valid: bool = False
    is_fixed_size: bool = False
    semantic_type: uint64 = 0
    frame_size: uint64 = 0
    width: uint32 = 0
    height: uint32 = 0
    bits_per_element: uint32 = 0
    stride: uint32 = 0
    properties: sequence[BufferInfoProperty] = field(default_factory=list)
