class MessageError(Exception):
    INVALID_PAYLOAD = "InvalidPayload"
    UNKNOWN_REPRESENTATION = "UnknownRepresentation"
    DECODING_ERROR = "DecodingError"
    MISSING_INFORMATION = "MissingInformation"
    NETWORK_ERROR = "NetworkError"
    TASK_ERROR = "TaskError"

    def __init__(self, kind: str, detail: str = ""):
        self.kind = kind
        self.detail = detail
        super().__init__(f"{kind}: {detail}")
