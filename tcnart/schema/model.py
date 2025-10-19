from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Union

from ..serialization.error import MessageError

# Import message classes to annotate union type
from .messages.stream import StreamDescriptorMessage
from .messages.video import VideoStreamMessage
from .messages.geometry import MeshBitstreamMessage
from .messages.monitor import (
    TcnartLogMessage,
    TcnartPresenceMessage,
    ApplicationEventMessage,
    ApplicationHealthStatusMessage,
    PerformanceMonitorMessage,
)
from .messages.camera import CameraSensorMessage
from .messages.service_controller import DeviceContextReply
from ..core.pixel_image import PixelImage
from .messages.common import InvalidMessage


MessageVariant = Union[
    InvalidMessage,
    StreamDescriptorMessage,
    VideoStreamMessage,
    MeshBitstreamMessage,
    TcnartLogMessage,
    ApplicationEventMessage,
    ApplicationHealthStatusMessage,
    PerformanceMonitorMessage,
    TcnartPresenceMessage,
    CameraSensorMessage,
    DeviceContextReply,
    PixelImage,
]


@dataclass
class MessageSchema:
    value: MessageVariant

    def schema_name(self) -> str:
        v = self.value
        # Mirror Rust mapping
        if isinstance(v, StreamDescriptorMessage):
            return "tcnart_msgs::msg::StreamDescriptorMessage"
        if isinstance(v, VideoStreamMessage):
            return "tcnart_msgs::msg::VideoStreamMessage"
        if isinstance(v, MeshBitstreamMessage):
            return "pcpd_msgs::msg::MeshBitstreamMessage"
        if isinstance(v, TcnartLogMessage):
            return "tcnart_msgs::msg::TcnartLogMessage"
        if isinstance(v, ApplicationEventMessage):
            return "tcnart_msgs::msg::ApplicationEventMessage"
        if isinstance(v, ApplicationHealthStatusMessage):
            return "tcnart_msgs::msg::ApplicationHealthStatusMessage"
        if isinstance(v, PerformanceMonitorMessage):
            return "tcnart_msgs::msg::PerformanceMonitorMessage"
        if isinstance(v, TcnartPresenceMessage):
            return "tcnart_msgs::msg::TcnartPresenceMessage"
        if isinstance(v, CameraSensorMessage):
            return "pcpd_msgs::msg::CameraSensor"
        if isinstance(v, DeviceContextReply):
            return "pcpd_msgs::msg::DeviceContextReply"
        if isinstance(v, PixelImage):
            return "tcnart_msgs::msg::PixelImage"
        if isinstance(v, InvalidMessage):
            raise MessageError(MessageError.INVALID_PAYLOAD)
        raise MessageError(MessageError.MISSING_INFORMATION, "Unknown schema type")

    @staticmethod
    def get_timestamp(value: MessageVariant) -> int:
        # Each message implements get_timestamp(); keep simple duck-typing
        if hasattr(value, "get_timestamp"):
            return int(value.get_timestamp())
        raise MessageError(MessageError.MISSING_INFORMATION, "Message has no timestamp")
