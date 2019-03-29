from __future__ import annotations
import random as r
from typing import TYPE_CHECKING
from main.block import Block
from main.justification import Justification
if TYPE_CHECKING:
    from main.validator import Validator
    from main.state import State


class Message:
    def __init__(
        self,
        sender: Validator,
        estimate: Block,
        justification: Justification,
        sender_slot: int
    ):
        self.sender: Validator = sender
        self.estimate: Block = estimate
        self.justification: Justification = justification
        self.sender_slot: int = sender_slot
        # TODO: implement
        self.hash: int = r.randint(1, 100000000000000)

    @classmethod
    def genesis(cls, sender: Validator) -> Message:
        return Message(sender, Block.genesis(), Justification(), 0)

    def is_genesis(self) -> bool:
        return self.estimate.is_genesis()

    def dump(self, state: State = None, parent_message: Message = None):
        if parent_message is not None:
            parent_hash = parent_message.hash
        else:
            parent_hash = None
        return {
            "sender": self.sender.name,
            "estimate": self.estimate.dump(),
            "justification": self.justification.dump(state),
            "slot": self.sender_slot,
            "hash": self.hash,
            "parent_hash": parent_hash
        }