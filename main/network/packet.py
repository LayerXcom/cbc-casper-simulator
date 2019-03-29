import dataclasses
from main.message import Message
from main.validator import Validator


@dataclasses.dataclass
class Packet:
    message: Message
    sender: Validator
    receiver: Validator
    slot: int
