from __future__ import annotations
from typing import List
from cbc_casper_simulator.state import State
from cbc_casper_simulator.message import Message
from cbc_casper_simulator.message_validator import MessageValidator
from cbc_casper_simulator.justification import Justification
from cbc_casper_simulator.block import Block
from cbc_casper_simulator.estimator.lmd_ghost_estimator import LMDGhostEstimator as Estimator
from cbc_casper_simulator.util.ticker import Ticker
from cbc_casper_simulator.error import Error
import random as r
from result import Result


class Validator:
    def __init__(
            self,
            name: str,
            initial_weight: float,
            ticker: Ticker
    ):
        self.name: str = name
        self.weight: float = initial_weight
        self.state = State(ticker)
        # TODO: implement
        self.hash: int = r.randint(1, 100000000000000)

    def create_message(self) -> Message:
        sender: Validator = self
        estimate: Block = self.create_estimate()
        justification: Justification = self.state.justification()
        current_slot: int = self.state.current_slot()
        return Message(
            sender,
            estimate,
            justification,
            current_slot
        )

    def create_estimate(self) -> Block:
        head: Block = self.head()
        height: int = head.height + 1
        active_validators: List[Validator] = head.active_validators
        parent_hash: int = head.hash
        return Block(
            height,
            active_validators,
            parent_hash
        )

    def head(self) -> Block:
        # FIXME: Rename
        return Estimator.head(self.state, self.state.justification())

    def add_message(self, message: Message) -> Result[Error, bool]:
        return self.state.transition(message)

    def message_is_to_be_pending(self, message: Message) -> bool:
        return MessageValidator.justification_is_justified(self.state, message.justification).is_err()

    def tick(self):
        self.state.tick()

    @classmethod
    def gen_name(cls, message: Message, slot: int, checkpoint_interval: int, checkpoint_rotation_count: int) -> str:
        name_prefix = "{}.{}".format(int(message.estimate.height / checkpoint_interval), checkpoint_rotation_count)
        name = "v{}.{}".format(name_prefix, slot)
        return name

    def dump(self):
        return {
            "name": self.name,
            "state": self.state.dump(),
            "current_slot": self.state.ticker.current()
        }

    def __eq__(self, other: Validator):
        return self.hash == other.hash

    def __hash__(self):
        return self.hash
