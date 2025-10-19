from dataclasses import dataclass, field
from typing import List
from pycdr2 import IdlStruct, IdlEnum
from pycdr2.types import int32, uint32, float64, float32, sequence, uint8, uint16, uint64, array

from ..types.common import Header, Time
from ...serialization.cdr_serialization import register_type


class TcnartLogLevel(IdlEnum, typename="TcnartLogLevel"):
    Error = 0
    Warning = 1
    Info = 2
    Debug = 3
    Trace = 4


class ApplicationLifeCycleEventDomain(IdlEnum, typename="ApplicationLifeCycleEventDomain"):
    Application = 0
    CoreService = 1
    ConsumerService = 2
    ProducerService = 3
    Runtime = 4
    Dataflow = 5
    Component = 6


class ApplicationHealthStatusUpdate(IdlEnum, typename="ApplicationHealthStatusUpdate"):
    WatchdogEvent = 0
    CaptureDeviceTimeout = 1
    DiskSpaceWarning = 2
    LowLightWarning = 3
    LowFramerateWarning = 4
    WriteQueueWarning = 5
    FramerateInfo = 6
    ImuMovementWarning = 7


@dataclass
class TcnartLogItem(IdlStruct, typename="TcnartLogItem"):
    timestamp: Time = field(default_factory=Time)
    severity: TcnartLogLevel = TcnartLogLevel.Info
    message: str = ""


@dataclass
class TcnartLogMessage(IdlStruct, typename="TcnartLogMessage"):
    header: Header = field(default_factory=Header)
    items: List[TcnartLogItem] = field(default_factory=list)

    @staticmethod
    def new() -> "TcnartLogMessage":
        return TcnartLogMessage()

    def get_timestamp(self) -> int:
        return self.header.stamp.to_timestamp()


@dataclass
class PerformanceMonitorItem(IdlStruct, typename="PerformanceMonitorItem"):
    port_name: str = ""
    num_events: uint32 = 0
    total_events: uint64 = 0
    fps: float32 = 0.0
    realtime_ms: float32 = 0.0
    duration_mean_ms: float32 = 0.0
    duration_stddev_ms: float32 = 0.0


@dataclass
class PerformanceMonitorMessage(IdlStruct, typename="PerformanceMonitorMessage"):
    header: Header = field(default_factory=Header)
    dataflow_timestamp: uint64 = 0
    report_duration_ms: uint32 = 0
    items: List[PerformanceMonitorItem] = field(default_factory=list)

    @staticmethod
    def new() -> "PerformanceMonitorMessage":
        return PerformanceMonitorMessage()

    def get_timestamp(self) -> int:
        return self.header.stamp.to_timestamp()


class ApplicationLifeCycleStatus(IdlEnum, typename="ApplicationLifeCycleStatus"):
    Initialized = 0
    Started = 1
    Stopped = 2
    Uninitialized = 3


@dataclass
class ApplicationHealthStatusMessage(IdlStruct, typename="ApplicationHealthStatusMessage"):
    header: Header = field(default_factory=Header)
    domain: ApplicationLifeCycleEventDomain = ApplicationLifeCycleEventDomain.Application
    name: str = ""
    health_status: ApplicationHealthStatusUpdate = ApplicationHealthStatusUpdate.WatchdogEvent
    payload: bytes = b""

    @staticmethod
    def new() -> "ApplicationHealthStatusMessage":
        return ApplicationHealthStatusMessage()

    def get_timestamp(self) -> int:
        return self.header.stamp.to_timestamp()


@dataclass
class ApplicationEventMessage(IdlStruct, typename="ApplicationEventMessage"):
    header: Header = field(default_factory=Header)
    domain: ApplicationLifeCycleEventDomain = ApplicationLifeCycleEventDomain.Application
    name: str = ""
    event: ApplicationLifeCycleStatus = ApplicationLifeCycleStatus.Uninitialized

    @staticmethod
    def new() -> "ApplicationEventMessage":
        return ApplicationEventMessage()

    def get_timestamp(self) -> int:
        return self.header.stamp.to_timestamp()


@dataclass
class ServiceInfo(IdlStruct, typename="ServiceInfo"):
    service_name: str = ""
    topic_prefix: str = ""
    service_info: str = ""

    @staticmethod
    def new() -> "ServiceInfo":
        return ServiceInfo()


@dataclass
class TcnartPresenceMessage(IdlStruct, typename="TcnartPresenceMessage"):
    header: Header = field(default_factory=Header)
    heart_beat_counter: uint64 = 0
    services: List[ServiceInfo] = field(default_factory=list)

    @staticmethod
    def new() -> "TcnartPresenceMessage":
        return TcnartPresenceMessage()

    def get_timestamp(self) -> int:
        return self.header.stamp.to_timestamp()


# Register schema type names
register_type("tcnart_msgs::msg::TcnartLogMessage", TcnartLogMessage)
register_type("tcnart_msgs::msg::PerformanceMonitorMessage", PerformanceMonitorMessage)
register_type("tcnart_msgs::msg::ApplicationHealthStatusMessage", ApplicationHealthStatusMessage)
register_type("tcnart_msgs::msg::ApplicationEventMessage", ApplicationEventMessage)
register_type("tcnart_msgs::msg::TcnartPresenceMessage", TcnartPresenceMessage)
