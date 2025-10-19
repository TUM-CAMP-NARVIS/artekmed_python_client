from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

from ..serialization.cdr_serialization import register_type


@dataclass
class PixelImage:
    # Minimal Python reimplementation of Rust PixelImage for schema usage.
    # We represent semantic_type as a 64-bit integer identifier.
    semantic_type: int = 0
    width: int = 0
    height: int = 0
    image_buffer: bytes = field(default_factory=bytes)

    @staticmethod
    def new() -> "PixelImage":
        return PixelImage()

    @staticmethod
    def with_params(semantic_type: int, width: int, height: int, image_data: bytes) -> "PixelImage":
        return PixelImage(semantic_type=semantic_type, width=width, height=height, image_buffer=bytes(image_data))

    # Optional helpers to attach raw CDR payload if needed by serializer fallback
    def to_cdr(self, endianness: str = "little") -> bytes:
        # This class does not define an IDL mapping. Leave to higher-level code.
        # Provide a clear error to prompt explicit encoding if attempted.
        raise RuntimeError("PixelImage.to_cdr not implemented; provide raw CDR payload externally")

    @classmethod
    def from_cdr(cls, buffer: bytes, endianness: str = "little") -> "PixelImage":
        # Without IDL, we cannot decode. Return an empty image and attach raw payload externally if needed.
        inst = cls.new()
        setattr(inst, "_raw_cdr_payload", buffer)
        setattr(inst, "_raw_cdr_endianness", endianness)
        return inst


# Register schema type name mapping for PixelImage to enable decode_raw_message
register_type("tcnart_msgs::msg::PixelImage", PixelImage)
