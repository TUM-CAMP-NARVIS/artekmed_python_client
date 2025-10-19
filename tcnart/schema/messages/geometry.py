from dataclasses import dataclass, field

from ..types.common import Header
from ..types.transform import RigidTransform
from ...serialization.cdr_serialization import register_type
from pycdr2 import IdlStruct
from pycdr2.types import int32, uint32, float64, float32, sequence, uint8, uint16, uint64, array


@dataclass
class MeshBitstreamMessage(IdlStruct, typename="MeshBitstreamMessage"):
    header: Header = field(default_factory=Header)
    origin_offset: RigidTransform = field(default_factory=RigidTransform)
    enable_mesh_indices: bool = False
    is_compressed: bool = False
    num_camera_ids: uint32 = 0
    vertices_capacity: uint64 = 0
    faces_capacity: uint64 = 0
    vertex_size_bytes: uint64 = 0
    num_vertices: uint64 = 0
    num_faces: uint64 = 0
    data_bytes: uint64 = 0
    data: sequence[uint8] = field(default_factory=list)

    @staticmethod
    def new() -> "MeshBitstreamMessage":
        return MeshBitstreamMessage()

    def get_timestamp(self) -> int:
        return self.header.stamp.to_timestamp()


# Register schema type name
register_type("pcpd_msgs::msg::MeshBitstreamMessage", MeshBitstreamMessage)
