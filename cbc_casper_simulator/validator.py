from __future__ import annotations
from typing import List
from cbc_casper_simulator.state import State
from cbc_casper_simulator.message import Message
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
        head: Block = Estimator.head(self.state, self.state.justification())
        height: int = head.height + 1
        active_validators: List[Validator] = head.active_validators
        parent_hash: int = head.hash
        return Block(
            height,
            active_validators,
            parent_hash
        )

    def add_message(self, message: Message) -> Result[Error, bool]:
        return self.state.transition(message)

    def tick(self):
        self.state.tick()

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
