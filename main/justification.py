from typing import Dict
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main.validator import Validator


class Justification:
    def __init__(
        self,
        latest_messages: Dict['Validator', int] = dict()
    ):
        self.latest_messages: Dict[Validator, int] = latest_messages

    def dump(self, state: 'State'):
        return [
            {
                "sender": v.name,
                "message_hash": message_hash
            }
            for v, message_hash in self.latest_messages.items()
        ]
