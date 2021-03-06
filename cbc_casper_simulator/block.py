from __future__ import annotations
from typing import Optional, List
import random as r
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cbc_casper_simulator.validator import Validator


class Block:
    def __init__(
        self,
        height: int,
        active_validators: List[Validator] = [],
        parent_hash: Optional[int] = None
    ):
        self.height = height
        self.parent_hash: Optional[int] = parent_hash
        self.active_validators: List[Validator] = active_validators
        # TODO: random_number is appropriate?
        self.hash: int = r.randint(1, 100000000000000)

    @classmethod
    def genesis(cls, active_validators: List[Validator]) -> Block:
        return Block(0, active_validators)

    def is_genesis(self) -> bool:
        return self.parent_hash is None

    def is_checkpoint(self, checkpoint_interval: int) -> bool:
        return self.height > 0 and self.height % checkpoint_interval == 0

    def dump(self):
        return {
            "height": self.height,
            "parent_hash": self.parent_hash,
            "hash": self.hash,
            "active_validators": [v.name for v in self.active_validators]
        }
