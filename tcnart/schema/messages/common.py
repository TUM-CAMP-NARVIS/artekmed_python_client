from dataclasses import dataclass


@dataclass
class InvalidMessage:
    def get_timestamp(self) -> int:
        return 0
