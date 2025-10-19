from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Any

from ..schema.messages.common import InvalidMessage
from ..schema.types.common import BufferInfo
from ..schema.types.primitives import CameraModel


@dataclass
class FrameAnnotation:
    kind: str
    value: Any

    @staticmethod
    def camera_model(value: CameraModel) -> "FrameAnnotation":
        return FrameAnnotation("CameraModel", value)

    @staticmethod
    def buffer_info(value: BufferInfo) -> "FrameAnnotation":
        return FrameAnnotation("BufferInfo", value)

    @staticmethod
    def semantic_type(value: int) -> "FrameAnnotation":
        return FrameAnnotation("SemanticType", value)

    @staticmethod
    def sensor_pose(isometry3: Any) -> "FrameAnnotation":
        # Placeholder type for isometry (no nalgebra in Python port)
        return FrameAnnotation("SensorPose", isometry3)

    @staticmethod
    def camera_intrinsics(matrix3: Any) -> "FrameAnnotation":
        return FrameAnnotation("CameraIntrinsics", matrix3)

    @staticmethod
    def distortion_coefficients(coeffs: List[float]) -> "FrameAnnotation":
        return FrameAnnotation("DistortionCoefficients", list(coeffs))


@dataclass
class Frame:
    timestamp: int = 0
    semantic_type: int = 0  # Using identifier u64 equivalent
    stream_id: int = 0
    data: Any = field(default_factory=InvalidMessage)
    annotations: Dict[str, FrameAnnotation] = field(default_factory=dict)

    @staticmethod
    def new() -> "Frame":
        return Frame()

    @staticmethod
    def create(timestamp: int, semantic_type: int, stream_id: int, data: Any) -> "Frame":
        return Frame(timestamp=timestamp, semantic_type=semantic_type, stream_id=stream_id, data=data)

    def is_complete(self) -> bool:
        return not isinstance(self.data, InvalidMessage) and self.timestamp != 0

    # Setters
    def set_timestamp(self, timestamp: int) -> None:
        self.timestamp = int(timestamp)

    def set_semantic_type(self, semantic_type: int) -> None:
        self.semantic_type = int(semantic_type)

    def set_stream_id(self, stream_id: int) -> None:
        self.stream_id = int(stream_id)

    def set_data(self, data: Any) -> None:
        self.data = data

    # Getters
    def get_timestamp(self) -> int: return int(self.timestamp)
    def get_semantic_type(self) -> int: return int(self.semantic_type)
    def get_stream_id(self) -> int: return int(self.stream_id)
    def get_data(self) -> Any: return self.data

    # Annotations
    def add_annotation(self, key: str, value: FrameAnnotation) -> None:
        self.annotations[key] = value

    def get_annotation(self, key: str) -> Optional[FrameAnnotation]:
        return self.annotations.get(key)

    def get_annotations(self) -> Dict[str, FrameAnnotation]:
        return self.annotations


# Timestamp helpers
class TimestampIter:
    def __init__(self, frames_map: Dict[str, int | Frame]):
        self._iter = iter(frames_map.items())

    def __iter__(self) -> "TimestampIter":
        return self

    def __next__(self) -> int:
        _, v = next(self._iter)
        if isinstance(v, Frame):
            return v.get_timestamp()
        return int(v)


def timestamp_iter(frames_map: Dict[str, int | Frame]) -> Iterator[int]:
    return iter(TimestampIter(frames_map))


class TimestampMatcher:
    def check_timestamp(self, timestamp: int, timestamps: Iterable[int]) -> bool:
        raise NotImplementedError


@dataclass
class TimestampMatcherExact(TimestampMatcher):
    def check_timestamp(self, timestamp: int, timestamps: Iterable[int]) -> bool:
        for ts in timestamps:
            if ts != 0 and ts != timestamp:
                return False
        return True


@dataclass
class TimestampMatcherWindow(TimestampMatcher):
    max_offset_ms: int

    def check_timestamp(self, timestamp: int, timestamps: Iterable[int]) -> bool:
        offset_ns = int(self.max_offset_ms) * 1_000_000
        for ts in timestamps:
            if ts == 0:
                continue
            diff = abs(int(ts) - int(timestamp))
            if diff > offset_ns:
                return False
        return True


@dataclass
class TimestampMatcherType(TimestampMatcher):
    exact: Optional[TimestampMatcherExact] = None
    window: Optional[TimestampMatcherWindow] = None

    @staticmethod
    def new_exact() -> "TimestampMatcherType":
        return TimestampMatcherType(exact=TimestampMatcherExact())

    @staticmethod
    def new_window(max_offset_ms: int) -> "TimestampMatcherType":
        return TimestampMatcherType(window=TimestampMatcherWindow(max_offset_ms=max_offset_ms))

    def get_exact(self) -> Optional[TimestampMatcherExact]:
        return self.exact

    def get_window(self) -> Optional[TimestampMatcherWindow]:
        return self.window

    def check_timestamp(self, timestamp: int, timestamps: Iterable[int]) -> bool:
        if self.exact is not None:
            return self.exact.check_timestamp(timestamp, timestamps)
        if self.window is not None:
            return self.window.check_timestamp(timestamp, timestamps)
        # Default to exact if none provided
        return TimestampMatcherExact().check_timestamp(timestamp, timestamps)


@dataclass
class GroupOfFrames:
    ref_timestamp: int = 0
    frames: Dict[str, Frame] = field(default_factory=dict)

    @staticmethod
    def new(timestamp: int, channels: List[str]) -> "GroupOfFrames":
        frames = {ch: Frame.new() for ch in channels}
        return GroupOfFrames(ref_timestamp=timestamp, frames=frames)

    def set_frame(self, channel: str, frame: Frame) -> None:
        self.frames[channel] = frame

    def get_frames(self) -> Dict[str, Frame]:
        return self.frames

    def get_frame(self, channel: str) -> Optional[Frame]:
        return self.frames.get(channel)

    def get_ref_timestamp(self) -> int:
        return int(self.ref_timestamp)

    def max_timestamp(self) -> int:
        max_ts = 0
        for _, f in self.frames.items():
            ts = f.get_timestamp()
            if ts > max_ts:
                max_ts = ts
        return max_ts

    def min_timestamp(self) -> int:
        min_ts = 0
        for _, f in self.frames.items():
            ts = f.get_timestamp()
            if ts < min_ts:
                min_ts = ts
        return min_ts

    def is_complete(self) -> bool:
        # All channels must have a complete frame
        return all(f.is_complete() for f in self.frames.values())


# Synchronous approximation of Rust dataflow timestamp_grouper
# This function groups an iterable of Frame into GroupOfFrames given the channel order.

def timestamp_grouper(frames: Iterable[Frame], worker_channels: List[str], matcher: Optional[TimestampMatcherType] = None) -> List[GroupOfFrames]:
    if matcher is None:
        matcher = TimestampMatcherType.new_exact()

    unfinished: Dict[int, GroupOfFrames] = {}
    out: List[GroupOfFrames] = []

    for frame in frames:
        if not frame.is_complete():
            continue
        ts = frame.get_timestamp()
        stream_id = frame.get_stream_id()
        channel = worker_channels[stream_id]

        matched_ts = 0
        for ref_ts, group in list(unfinished.items()):
            if matcher.check_timestamp(ts, (f.get_timestamp() for f in group.get_frames().values())):
                matched_ts = ref_ts
                break

        if matched_ts == 0:
            unfinished[ts] = GroupOfFrames.new(ts, worker_channels)
            matched_ts = ts

        group = unfinished[matched_ts]
        group.set_frame(channel, frame)

        # Find completed groups and emit them in ascending timestamp order
        completed = sorted([ref for ref, grp in unfinished.items() if grp.is_complete()])
        latest_ts = 0
        for ref in completed:
            grp = unfinished.pop(ref)
            out.append(grp)
            latest_ts = max(latest_ts, grp.max_timestamp())

        if latest_ts != 0:
            # Retain only groups whose max_timestamp >= latest_ts
            # XXX NOT SAVED!!
            unfinished = {ref: grp for ref, grp in unfinished.items() if grp.max_timestamp() >= latest_ts}

    return out
