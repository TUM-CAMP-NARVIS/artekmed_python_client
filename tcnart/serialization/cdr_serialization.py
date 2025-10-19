from __future__ import annotations
from typing import Tuple, Dict, Type, Any

from .error import MessageError
from ..schema.messages.common import InvalidMessage

import pycdr2

MIN_PAYLOAD_SIZE = 4

# Registry for schema type name -> Python class factory
_TYPE_REGISTRY: Dict[str, Any] = {}


def register_type(name: str, cls: Any) -> None:
    _TYPE_REGISTRY[name] = cls


def decode_raw_message(type_name: str, payload: bytes) -> Any:
    # lookup target class
    cls = _TYPE_REGISTRY.get(type_name)
    if cls is None:
        # fall back to InvalidMessage
        return InvalidMessage()

    # pycdr2 usage placeholder; requires IDL/type definitions to fully decode.
    # We provide an extension point for classes to implement classmethod from_cdr(buffer: bytes, endianness: str) -> Any
    if hasattr(cls, "deserialize") and callable(getattr(cls, "deserialize")):
        try:
            return cls.deserialize(payload)
        except Exception as e:  # surface as decoding error
            raise MessageError(MessageError.DECODING_ERROR, str(e))

    return InvalidMessage()


def encode_raw_message(message: Any, type_name: str | None = None) -> bytes:

    # Allow message to provide its own encoder
    if hasattr(message, "serialize") and callable(getattr(message, "serialize")):
        try:
            payload = message.serialize()  # expected to return bytes
            return payload
        except Exception as e:
            raise MessageError(MessageError.DECODING_ERROR, str(e))

    # If we cannot produce CDR, raise a clear error to prompt explicit to_cdr implementation
    raise MessageError(MessageError.DECODING_ERROR, "No serialize() provided and no raw CDR payload available")


def get_message_schema_name(message: Any) -> str:
    # Mirror Rust get_message_schema_name for known wrapper types
    from ..schema.model import MessageSchema
    if isinstance(message, MessageSchema):
        return message.schema_name()
    raise MessageError(MessageError.MISSING_INFORMATION, "Unsupported message wrapper type")
