from dataclasses import dataclass, field
from typing import List, Union
from pycdr2 import IdlStruct, IdlEnum
from pycdr2.types import int32, int64, uint32, float64, float32, sequence, uint8, uint16, uint64, array


class RPCResponseStatus(IdlEnum, typename="RPCResponseStatus"):
    RpcStatusSuccess = 0
    RpcStatusError = 1


class ParameterValueType(IdlEnum, typename="ParameterValueType"):
    PvtString = 0
    PvtInt32 = 1
    PvtInt64 = 2
    PvtFloat = 3
    PvtDouble = 4
    PvtBool = 5
    PvtStruct = 6


@dataclass
class Parameter(IdlStruct, typename="Parameter"):
    key: str = ""
    value: "ParameterValue" = None  # type: ignore


@dataclass
class ParameterList(IdlStruct, typename="ParameterList"):
    parameters: List[Parameter] = field(default_factory=list)


ParameterValue = Union[
    str,
    int32,
    int64,
    float32,
    float64,
    bool,
    ParameterList,
]


@dataclass
class ParameterSchema(IdlStruct, typename="ParameterSchema"):
    key: str = ""
    value_type: ParameterValueType = ParameterValueType.PvtString
    valid_entries: List[Union[str, int32, int64, float32, float64, bool]] = field(default_factory=list)


@dataclass
class ParameterListSchema(IdlStruct, typename="ParameterListSchema"):
    parameters: List[ParameterSchema] = field(default_factory=list)


# Simple request/reply types
@dataclass
class NullRequest(IdlStruct, typename="NullRequest"):
    dummy: uint8 = 0


@dataclass
class NullReply(IdlStruct, typename="NullReply"):
    status: RPCResponseStatus = RPCResponseStatus.RpcStatusSuccess


@dataclass
class StringRequest(IdlStruct, typename="StringRequest"):
    value: str = ""


@dataclass
class StringReply(IdlStruct, typename="StringReply"):
    value: str = ""
    status: RPCResponseStatus = RPCResponseStatus.RpcStatusSuccess


@dataclass
class BoolRequest(IdlStruct, typename="BoolRequest"):
    value: bool = False


@dataclass
class BoolReply(IdlStruct, typename="BoolReply"):
    value: bool = False
    status: RPCResponseStatus = RPCResponseStatus.RpcStatusSuccess


@dataclass
class UInt32Request(IdlStruct, typename="UInt32Request"):
    value: uint32 = 0


@dataclass
class UInt32Reply(IdlStruct, typename="UInt32Reply"):
    value: uint32 = 0
    status: RPCResponseStatus = RPCResponseStatus.RpcStatusSuccess


@dataclass
class UInt64Request(IdlStruct, typename="UInt64Request"):
    value: uint64 = 0


@dataclass
class UInt64Reply(IdlStruct, typename="UInt64Reply"):
    value: uint64 = 0
    status: RPCResponseStatus = RPCResponseStatus.RpcStatusSuccess


@dataclass
class Int32Request(IdlStruct, typename="Int32Request"):
    value: int32 = 0


@dataclass
class Int32Reply(IdlStruct, typename="Int32Reply"):
    value: int32 = 0
    status: RPCResponseStatus = RPCResponseStatus.RpcStatusSuccess


@dataclass
class Int64Request(IdlStruct, typename="Int64Request"):
    value: int64 = 0


@dataclass
class Int64Reply(IdlStruct, typename="Int64Reply"):
    value: int64 = 0
    status: RPCResponseStatus = RPCResponseStatus.RpcStatusSuccess


@dataclass
class Float32Request(IdlStruct, typename="Float32Request"):
    value: float32 = 0.0


@dataclass
class Float32Reply(IdlStruct, typename="Float32Reply"):
    value: float32 = 0.0
    status: RPCResponseStatus = RPCResponseStatus.RpcStatusSuccess


@dataclass
class Float64Request(IdlStruct, typename="Float64Request"):
    value: float64 = 0.0


@dataclass
class Float64Reply(IdlStruct, typename="Float64Reply"):
    value: float64 = 0.0
    status: RPCResponseStatus = RPCResponseStatus.RpcStatusSuccess


@dataclass
class StringListRequest(IdlStruct, typename="StringListRequest"):
    values: List[str] = field(default_factory=list)


@dataclass
class StringListReply(IdlStruct, typename="StringListReply"):
    values: List[str] = field(default_factory=list)
    status: RPCResponseStatus = RPCResponseStatus.RpcStatusSuccess


@dataclass
class GenericParameterRequest(IdlStruct, typename="GenericParameterRequest"):
    value: ParameterList = field(default_factory=ParameterList)


@dataclass
class GenericParameterReply(IdlStruct, typename="GenericParameterReply"):
    value: ParameterList = field(default_factory=ParameterList)
    status: RPCResponseStatus = RPCResponseStatus.RpcStatusSuccess


@dataclass
class ParameterSchemaReply(IdlStruct, typename="ParameterSchemaReply"):
    schema: ParameterListSchema = field(default_factory=ParameterListSchema)
    status: RPCResponseStatus = RPCResponseStatus.RpcStatusSuccess
