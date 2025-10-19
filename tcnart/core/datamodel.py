from __future__ import annotations
from typing import Final

from .semantic_type.model import (
    constants,
    IdentifierStorageType,
    ScalarType,
    CardinalityType,
    ContainerType,
    MemoryRepresentationType,
    ContentTypes,
    ImageCompressionTypes,
    ImageFormatTypes,
    EmptyCustomType,
    GeometryCompressionTypes,
    GeometryFormatTypes,
    GeometryAttributes,
    TransformCompressionTypes,
    TransformFormatTypes,
    TransformDetailTypes,
)


# Image types
class image_types:
    @staticmethod
    def create_image_type(
        scalar_type: ScalarType,
        compression_type: ImageCompressionTypes,
        format_type: ImageFormatTypes,
    ) -> IdentifierStorageType:
        if compression_type == ImageCompressionTypes.None_:
            base_mrt = MemoryRepresentationType.None_
        elif compression_type == ImageCompressionTypes.Uncompressed:
            base_mrt = MemoryRepresentationType.Raw
        else:
            base_mrt = MemoryRepresentationType.Compressed

        base_id = image_types._create_base_id(
            scalar_type, CardinalityType.Fixed, ContainerType.Array2D, base_mrt
        )
        return (
            base_id
            | (ContentTypes.Image.value << constants.CONTENT_TYPE_OFFSET)
            | (compression_type.value << constants.COMPRESSION_TYPE_OFFSET)
            | (format_type.value << constants.FORMAT_TYPE_OFFSET)
            | (EmptyCustomType.None_.value << constants.CUSTOM1_TYPE_OFFSET)
            | (EmptyCustomType.None_.value << constants.CUSTOM2_TYPE_OFFSET)
            | (0 << constants.CUSTOM_MASK_TYPE_OFFSET)
        )

    @staticmethod
    def _create_base_id(
        scalar_type: ScalarType,
        cardinality_type: CardinalityType,
        container_type: ContainerType,
        memory_representation_type: MemoryRepresentationType,
    ) -> IdentifierStorageType:
        st_value = scalar_type.value << constants.SCALAR_TYPE_OFFSET
        cat_value = cardinality_type.value << constants.CARDINALITY_TYPE_OFFSET
        ct_value = container_type.value << constants.CONTAINER_TYPE_OFFSET
        mrt_value = memory_representation_type.value << constants.MEMORY_REPRESENTATION_TYPE_OFFSET
        return (st_value | cat_value | ct_value | mrt_value)

    # Predefined constants mirroring Rust
    GENERIC_IMAGE_2D: Final[int] = create_image_type.__func__(ScalarType.None_, ImageCompressionTypes.None_, ImageFormatTypes.None_)
    GENERIC_UNCOMPRESSED_IMAGE_2D: Final[int] = create_image_type.__func__(ScalarType.None_, ImageCompressionTypes.Uncompressed, ImageFormatTypes.None_)
    GENERIC_H264_BITSTREAM_IMAGE_2D: Final[int] = create_image_type.__func__(ScalarType.None_, ImageCompressionTypes.H264, ImageFormatTypes.None_)
    GENERIC_H265_BITSTREAM_IMAGE_2D: Final[int] = create_image_type.__func__(ScalarType.None_, ImageCompressionTypes.H265, ImageFormatTypes.None_)
    BGRA_UNCOMPRESSED_IMAGE_2D: Final[int] = create_image_type.__func__(ScalarType.UChar, ImageCompressionTypes.Uncompressed, ImageFormatTypes.Bgra)
    BGR_UNCOMPRESSED_IMAGE_2D: Final[int] = create_image_type.__func__(ScalarType.UChar, ImageCompressionTypes.Uncompressed, ImageFormatTypes.Bgr)
    RGBA_UNCOMPRESSED_IMAGE_2D: Final[int] = create_image_type.__func__(ScalarType.UChar, ImageCompressionTypes.Uncompressed, ImageFormatTypes.Rgba)
    RGB_UNCOMPRESSED_IMAGE_2D: Final[int] = create_image_type.__func__(ScalarType.UChar, ImageCompressionTypes.Uncompressed, ImageFormatTypes.Rgb)
    RGB_JPEG_IMAGE_2D: Final[int] = create_image_type.__func__(ScalarType.UChar, ImageCompressionTypes.Jpeg, ImageFormatTypes.Rgb)
    BGR_JPEG_IMAGE_2D: Final[int] = create_image_type.__func__(ScalarType.UChar, ImageCompressionTypes.Jpeg, ImageFormatTypes.Bgr)
    DEPTH_UNCOMPRESSED_IMAGE_2D: Final[int] = create_image_type.__func__(ScalarType.UInt16, ImageCompressionTypes.Uncompressed, ImageFormatTypes.Depth)
    DEPTH_ZDEPTH_COMPRESSED_IMAGE_2D: Final[int] = create_image_type.__func__(ScalarType.UInt16, ImageCompressionTypes.Zdepth, ImageFormatTypes.Depth)
    INFRARED_UNCOMPRESSED_IMAGE_2D: Final[int] = create_image_type.__func__(ScalarType.UInt16, ImageCompressionTypes.Uncompressed, ImageFormatTypes.Luminance)
    DEPTH_WEIGHTS_UNCOMPRESSED_IMAGE_2D: Final[int] = create_image_type.__func__(ScalarType.Float32, ImageCompressionTypes.Uncompressed, ImageFormatTypes.Luminance)
    MASK_UNCOMPRESSED_IMAGE_2D: Final[int] = create_image_type.__func__(ScalarType.UChar, ImageCompressionTypes.Uncompressed, ImageFormatTypes.Luminance)
    BODY_TRACKING_INDEX_UNCOMPRESSED_IMAGE_2D: Final[int] = create_image_type.__func__(ScalarType.UChar, ImageCompressionTypes.Uncompressed, ImageFormatTypes.Luminance)


# Geometry types
class geometry_types:
    @staticmethod
    def create_geometry_type(
        scalar_type: ScalarType,
        compression_type: GeometryCompressionTypes,
        format_type: GeometryFormatTypes,
        attributes: int,
    ) -> IdentifierStorageType:
        # Map compression to base MRT
        if compression_type == GeometryCompressionTypes.None_:
            base_mrt = MemoryRepresentationType.None_
        elif compression_type == GeometryCompressionTypes.Uncompressed:
            base_mrt = MemoryRepresentationType.Raw
        else:
            base_mrt = MemoryRepresentationType.Compressed

        base_id = geometry_types._create_base_id(
            scalar_type, CardinalityType.Fixed, ContainerType.Array1D, base_mrt
        )
        return (
            base_id
            | (ContentTypes.Geometry.value << constants.CONTENT_TYPE_OFFSET)
            | (compression_type.value << constants.COMPRESSION_TYPE_OFFSET)
            | (format_type.value << constants.FORMAT_TYPE_OFFSET)
            | (EmptyCustomType.None_.value << constants.CUSTOM1_TYPE_OFFSET)
            | (EmptyCustomType.None_.value << constants.CUSTOM2_TYPE_OFFSET)
            | (attributes << constants.CUSTOM_MASK_TYPE_OFFSET)
        )

    @staticmethod
    def _create_base_id(
        scalar_type: ScalarType,
        cardinality_type: CardinalityType,
        container_type: ContainerType,
        memory_representation_type: MemoryRepresentationType,
    ) -> IdentifierStorageType:
        st_value = scalar_type.value << constants.SCALAR_TYPE_OFFSET
        cat_value = cardinality_type.value << constants.CARDINALITY_TYPE_OFFSET
        ct_value = container_type.value << constants.CONTAINER_TYPE_OFFSET
        mrt_value = memory_representation_type.value << constants.MEMORY_REPRESENTATION_TYPE_OFFSET
        return (st_value | cat_value | ct_value | mrt_value)

    # Predefined geometry types
    POINT_CLOUD_VERTEX_NORMAL: Final[int] = create_geometry_type.__func__(
        ScalarType.Float32, GeometryCompressionTypes.Uncompressed, GeometryFormatTypes.Point,
        GeometryAttributes.Position.value | GeometryAttributes.Normal.value
    )

    SURFEL: Final[int] = create_geometry_type.__func__(
        ScalarType.Float32, GeometryCompressionTypes.Uncompressed, GeometryFormatTypes.Point,
        GeometryAttributes.Position.value | GeometryAttributes.Normal.value | GeometryAttributes.Radius.value
    )

    VOXELIZER_EXTRA_DATA: Final[int] = create_geometry_type.__func__(
        ScalarType.Float32, GeometryCompressionTypes.Uncompressed, GeometryFormatTypes.Point,
        GeometryAttributes.Position.value | GeometryAttributes.Covariance.value
    )

    MESH_VERTEX: Final[int] = create_geometry_type.__func__(
        ScalarType.Float32, GeometryCompressionTypes.Uncompressed, GeometryFormatTypes.SurfaceMesh,
        GeometryAttributes.Position.value
    )

    MESH_FACE: Final[int] = create_geometry_type.__func__(
        ScalarType.UInt32, GeometryCompressionTypes.Uncompressed, GeometryFormatTypes.SurfaceMesh,
        GeometryAttributes.Face.value
    )

    CAMERA_IDS: Final[int] = create_geometry_type.__func__(
        ScalarType.UChar, GeometryCompressionTypes.Uncompressed, GeometryFormatTypes.SurfaceMesh,
        GeometryAttributes.Id.value
    )

    TEXTURE_COORDINATES: Final[int] = create_geometry_type.__func__(
        ScalarType.Float32, GeometryCompressionTypes.Uncompressed, GeometryFormatTypes.SurfaceMesh,
        GeometryAttributes.TextureCoordinate.value
    )

    UNTEXTURED_SURFACE_MESH: Final[int] = create_geometry_type.__func__(
        ScalarType.Float32, GeometryCompressionTypes.Uncompressed, GeometryFormatTypes.SurfaceMesh,
        GeometryAttributes.Position.value | GeometryAttributes.Face.value
    )

    DRACO_COMPRESSED_MESH: Final[int] = create_geometry_type.__func__(
        ScalarType.UChar, GeometryCompressionTypes.Draco, GeometryFormatTypes.SurfaceMesh,
        GeometryAttributes.Position.value | GeometryAttributes.Face.value
    )

    MESH_BITSTREAM: Final[int] = create_geometry_type.__func__(
        ScalarType.UChar, GeometryCompressionTypes.Uncompressed, GeometryFormatTypes.SurfaceMesh,
        GeometryAttributes.Position.value | GeometryAttributes.Face.value | GeometryAttributes.Id.value
    )


# Transform types
class transform_types:
    @staticmethod
    def create_transform_type(
        scalar_type: ScalarType,
        cardinality_type: CardinalityType,
        format_type: TransformFormatTypes,
        detail_type: TransformDetailTypes,
    ) -> IdentifierStorageType:
        base_id = transform_types._create_base_id(
            scalar_type, cardinality_type, ContainerType.Array1D, MemoryRepresentationType.Raw
        )
        return (
            base_id
            | (ContentTypes.Transform.value << constants.CONTENT_TYPE_OFFSET)
            | (TransformCompressionTypes.None_.value << constants.COMPRESSION_TYPE_OFFSET)
            | (format_type.value << constants.FORMAT_TYPE_OFFSET)
            | (detail_type.value << constants.CUSTOM1_TYPE_OFFSET)
            | (EmptyCustomType.None_.value << constants.CUSTOM2_TYPE_OFFSET)
            | (0 << constants.CUSTOM_MASK_TYPE_OFFSET)
        )

    @staticmethod
    def create_imu_sensor_type(
        scalar_type: ScalarType,
        format_type: TransformFormatTypes,
    ) -> IdentifierStorageType:
        base_id = transform_types._create_base_id(
            scalar_type, CardinalityType.Fixed, ContainerType.Scalar, MemoryRepresentationType.Raw
        )
        return (
            base_id
            | (ContentTypes.Transform.value << constants.CONTENT_TYPE_OFFSET)
            | (TransformCompressionTypes.None_.value << constants.COMPRESSION_TYPE_OFFSET)
            | (format_type.value << constants.FORMAT_TYPE_OFFSET)
            | (TransformDetailTypes.None_.value << constants.CUSTOM1_TYPE_OFFSET)
            | (EmptyCustomType.None_.value << constants.CUSTOM2_TYPE_OFFSET)
            | (0 << constants.CUSTOM_MASK_TYPE_OFFSET)
        )

    @staticmethod
    def _create_base_id(
        scalar_type: ScalarType,
        cardinality_type: CardinalityType,
        container_type: ContainerType,
        memory_representation_type: MemoryRepresentationType,
    ) -> IdentifierStorageType:
        st_value = scalar_type.value << constants.SCALAR_TYPE_OFFSET
        cat_value = cardinality_type.value << constants.CARDINALITY_TYPE_OFFSET
        ct_value = container_type.value << constants.CONTAINER_TYPE_OFFSET
        mrt_value = memory_representation_type.value << constants.MEMORY_REPRESENTATION_TYPE_OFFSET
        return (st_value | cat_value | ct_value | mrt_value)

    # Predefined transform types
    HUMAN_POSE_TRACKING: Final[int] = create_transform_type.__func__(
        ScalarType.Float32, CardinalityType.Variable, TransformFormatTypes.RigidTransform, TransformDetailTypes.KinectBodyTracking
    )

    IMU_SENSOR: Final[int] = create_imu_sensor_type.__func__(
        ScalarType.Float32, TransformFormatTypes.Acceleration
    )
