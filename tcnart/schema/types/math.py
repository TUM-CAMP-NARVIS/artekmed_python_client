from dataclasses import dataclass
from pycdr2 import IdlStruct
from pycdr2.types import int32, uint32, float64, float32, sequence, uint8, uint16, uint64, array


@dataclass
class Vector2(IdlStruct, typename="Vector2"):
    x: float64 = 0.0
    y: float64 = 0.0


@dataclass
class Vector3(IdlStruct, typename="Vector3"):
    x: float64 = 0.0
    y: float64 = 0.0
    z: float64 = 0.0


@dataclass
class Vector4(IdlStruct, typename="Vector4"):
    x: float64 = 0.0
    y: float64 = 0.0
    z: float64 = 0.0
    w: float64 = 0.0


@dataclass
class Quaternion(IdlStruct, typename="Quaternion"):
    x: float64 = 0.0
    y: float64 = 0.0
    z: float64 = 0.0
    w: float64 = 1.0


@dataclass
class Matrix4x4(IdlStruct, typename="Matrix4x4"):
    col0: array[float64, 4] = (1.0, 0.0, 0.0, 0.0)
    col1: array[float64, 4] = (0.0, 1.0, 0.0, 0.0)
    col2: array[float64, 4] = (0.0, 0.0, 1.0, 0.0)
    col3: array[float64, 4] = (0.0, 0.0, 0.0, 1.0)


@dataclass
class Matrix4x3(IdlStruct, typename="Matrix4x3"):
    col0: array[float64, 3] = (1.0, 0.0, 0.0)
    col1: array[float64, 3] = (0.0, 1.0, 0.0)
    col2: array[float64, 3] = (0.0, 0.0, 1.0)
    col3: array[float64, 3] = (0.0, 0.0, 0.0)


@dataclass
class Matrix3x3(IdlStruct, typename="Matrix3x3"):
    col0: array[float64, 3] = (1.0, 0.0, 0.0)
    col1: array[float64, 3] = (0.0, 1.0, 0.0)
    col2: array[float64, 3] = (0.0, 0.0, 1.0)


@dataclass
class Ray(IdlStruct, typename="Ray"):
    origin: Vector3 = Vector3()
    direction: Vector3 = Vector3(0.0, 0.0, 1.0)
