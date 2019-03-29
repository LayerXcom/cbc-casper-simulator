from __future__ import annotations
from main.state import State
from main.message import Message
from main.estimator.lmd_ghost_estimator import LMDGhostEstimator as Estimator
from main.util.ticker import Ticker
import random as r


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
        sender = self
        justification = self.state.justification()
        estimate = Estimator.estimate(self.state, justification)
        print(Estimator.score(self.state, justification))
        message = Message(
            sender,
            estimate,
            justification,
            self.state.current_slot()
        )
        return message

    def add_message(self, message: Message):
        self.state.transition(message)

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
