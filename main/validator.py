from main.state import State
from main.message import Message
from main.estimator.lmd_ghost_estimator import LMDGhostEstimator as Estimator
from main.ticker import Ticker


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

    def create_message(self) -> Message:
        sender = self
        justification = self.state.justification()
        estimate = Estimator.estimate(self.state, justification)
        message = Message(
            sender,
            estimate,
            justification,
            self.state.current_slot()
        )
        return message

    def state_transition(self, message: Message):
        self.state.transition(message)

    def tick(self):
        self.state.tick()

    def dump(self):
        return {
            "name": self.name,
            "state": self.state.dump(),
            "current_slot": self.state.ticker.current()
        }
