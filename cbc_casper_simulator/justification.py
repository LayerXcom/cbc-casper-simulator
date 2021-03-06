from typing import Dict
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cbc_casper_simulator.validator import Validator
    from cbc_casper_simulator.state import State


class Justification:
    def __init__(
        self,
        latest_message_hashes: Dict['Validator', int] = dict()
    ):
        self.latest_message_hashes: Dict[Validator, int] = latest_message_hashes

    def dump(self, state: 'State'):
        return [
            {
                "sender": v.name,
                "message_hash": message_hash
            }
            for v, message_hash in self.latest_message_hashes.items()
        ]
