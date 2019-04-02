from cbc_casper_simulator.justification import Justification
from cbc_casper_simulator.message import Message
from cbc_casper_simulator.block import Block
from cbc_casper_simulator.store import Store
from cbc_casper_simulator.message_validator import MessageValidator
from cbc_casper_simulator.safety_oracle.clique_oracle import CliqueOracle
from cbc_casper_simulator.util.ticker import Ticker
from cbc_casper_simulator.error import StateTransitionError
from typing import Optional
from result import Ok, Err, Result


class State:
    def __init__(self, ticker: Optional[Ticker]):
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
