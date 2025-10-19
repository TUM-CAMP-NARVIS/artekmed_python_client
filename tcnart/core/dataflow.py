from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Dict, Any

from .frames import Frame, GroupOfFrames, TimestampMatcherType, FrameAnnotation, timestamp_grouper as _timestamp_grouper


# Synchronous wrapper approximating Rust dataflow::timestamp_grouper
# In Python, we operate on in-memory iterables and return a list of groups.

def timestamp_grouper(frames: Iterable[Frame], worker_channels: List[str], matcher: Optional[TimestampMatcherType] = None) -> List[GroupOfFrames]:
    return _timestamp_grouper(frames, worker_channels, matcher)


@dataclass
class StreamConfig:
    stream_id: int
    stream_name: str
    stream_topic: str
    sensor_name: Optional[str] = None
    descriptor: Optional[Any] = None  # StreamDescriptorMessage
    annotations: Dict[str, FrameAnnotation] = field(default_factory=dict)

    @staticmethod
    def new(stream_id: int, stream_name: str, stream_topic: str) -> "StreamConfig":
        return StreamConfig(stream_id=stream_id, stream_name=stream_name, stream_topic=stream_topic)

    def add_annotation(self, key: str, value: FrameAnnotation) -> None:
        self.annotations[key] = value
