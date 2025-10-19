from dataclasses import dataclass, field
from pycdr2 import IdlStruct, IdlEnum
from pycdr2.types import int32, uint32, float64, float32, sequence, uint8, uint16, uint64, array
from enum import IntEnum

from typing import Tuple

from .math import Vector3, Quaternion
from .common import CameraModelType


@dataclass
class Plane(IdlStruct, typename="Plane"):
    normal: Vector3 = field(default_factory=Vector3)
    d: float32 = 0.0


@dataclass
class BoundingBox(IdlStruct, typename="BoundingBox"):
    center: Vector3 = field(default_factory=Vector3)
    extents: Vector3 = field(default_factory=Vector3)


@dataclass
class Frustum(IdlStruct, typename="Frustum"):
    plane_near: Plane = field(default_factory=Plane)
    plane_far: Plane = field(default_factory=Plane)
    plane_right: Plane = field(default_factory=Plane)
    plane_left: Plane = field(default_factory=Plane)
    plane_top: Plane = field(default_factory=Plane)
    plane_bottom: Plane = field(default_factory=Plane)


@dataclass
class OrientedBox(IdlStruct, typename="OrientedBox"):
    center: Vector3 = field(default_factory=Vector3)
    extents: Vector3 = field(default_factory=Vector3)
    orientation: Quaternion = field(default_factory=Quaternion)


@dataclass
class Sphere(IdlStruct, typename="Sphere"):
    center: Vector3 = field(default_factory=Vector3)
    radius: float32 = 0.0


@dataclass
class CameraModel(IdlStruct, typename="CameraModel"):
    camera_model: CameraModelType = CameraModelType.CameraModelNone
    image_width: uint16 = 0
    image_height: uint16 = 0
    focal_length: array[float64, 2] = (1.0, 1.0)
    principal_point: array[float64, 2] = (0.0, 0.0)
    tangential_coefficients: array[float64, 2] = (0.0, 0.0)
    radial_coefficients: array[float64, 8] = (
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    )
