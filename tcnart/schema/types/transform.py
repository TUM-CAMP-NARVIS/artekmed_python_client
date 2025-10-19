from dataclasses import dataclass, field
from pycdr2 import IdlStruct
from pycdr2.types import int32, uint32, float64, float32, sequence, uint8, uint16, uint64, array
from enum import IntEnum

from typing import List

from .math import Vector3, Quaternion


@dataclass
class RigidTransform(IdlStruct, typename="RigidTransform"):
    translation: Vector3 = field(default_factory=Vector3)
    rotation: Quaternion = field(default_factory=Quaternion)


@dataclass
class RigidTransformMapItem(IdlStruct, typename="RigidTransformMapItem"):
    item_id: uint32 = 0
    pose: RigidTransform = field(default_factory=RigidTransform)


@dataclass
class RigidTransformMap(IdlStruct, typename="RigidTransformMap"):
    pose: RigidTransform = field(default_factory=RigidTransform)
    poses: List[RigidTransformMapItem] = field(default_factory=list)


@dataclass
class ViewPose(IdlStruct, typename="ViewPose"):
    eye: Vector3 = field(default_factory=Vector3)
    target: Vector3 = field(default_factory=Vector3)
    up: Vector3 = field(default_factory=lambda: Vector3(0.0, 1.0, 0.0))
