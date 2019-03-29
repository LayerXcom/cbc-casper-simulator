from main.justification import Justification
from main.message import Message
from main.block import Block
from main.store import Store
from main.message_validator import MessageValidator
from main.safety_oracle.clique_oracle import CliqueOracle
from main.util.ticker import Ticker
from main.error import StateTransitionError
from typing import Optional
from result import Ok, Err, Result


class State:
    def __init__(self, ticker: Optional[Ticker]):
        self.last_finalized_block: Optional[Block] = None
        self.store: Store = Store()
        if ticker is None:
            self.ticker = Ticker()
        else:
            self.ticker = ticker

    def transition(self, message: Message) -> Result[StateTransitionError, bool]:
        # TODO: implement
        checked = self.check_message(message)
        if checked.is_err():
            return checked.Err()

        finalized = self.finalize_message(message)
        if finalized.is_err():
            return finalized.Err()

        return Ok(True)

    def check_message(self, message: Message) -> Result[StateTransitionError, bool]:
        if not MessageValidator.validate(self, message):
            return Err(StateTransitionError())

        if not CliqueOracle.check_safety(message.estimate, self, None):
            return Err(StateTransitionError())

        return Ok(True)

    def finalize_message(self, message: Message) -> Result[StateTransitionError, bool]:
        message.receiver_slot = self.ticker.current()
        self.last_finalized_block = message.estimate
        self.store.add(message)
        return Ok(True)

    def justification(self) -> Justification:
        return Justification(self.store.latest_messages())

    def dump(self):
        return {
            "messages": self.store.dump(self)
        }

    def tick(self):
        self.ticker.tick()

    def current_slot(self) -> int:
        return self.ticker.current()
