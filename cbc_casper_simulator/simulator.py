from __future__ import annotations
from typing import Iterable
from cbc_casper_simulator.message import Message
from cbc_casper_simulator.validator_set import ValidatorSet
from cbc_casper_simulator.network.model import Model as NetworkModel
from cbc_casper_simulator.util.ticker import Ticker


class SimulatorConfig:
    def __init__(
        self,
        validator_num: int,
        max_slot: int = 100
    ):
        self.validator_num = validator_num
        self.max_slot = max_slot

    @classmethod
    def default(cls) -> SimulatorConfig:
        return SimulatorConfig(3)


class RandomCreationAndBroadcastSimulator(Iterable[NetworkModel]):
    def __init__(self,
                 config: SimulatorConfig
                 ):
        self.config = config
        self.ticker = Ticker()
        validator_set = ValidatorSet.with_random_weight(
            config.validator_num, self.ticker)
        self.network = NetworkModel(validator_set, self.ticker)

    def __iter__(self):
        return self

    def __next__(self) -> NetworkModel:
        i = self.ticker.current()
        if i == 0:
            current = self.step_0()
        elif i > self.config.max_slot:
            raise StopIteration
        else:
            current = self.step_n()
        self.ticker.tick()
        return current

    def step_0(self) -> NetworkModel:
        # Add genesis message to all validators
        validator_set = self.network.validator_set
        genesis = Message.genesis(validator_set.choice_one())
        for validator in validator_set.all():
            validator.add_message(genesis)
        return self.network

    def step_n(self) -> NetworkModel:
        validator_set = self.network.validator_set
        if self.ticker.current() % 10 == 0:
            # The validator randomly selected create and broadcast a message to other validators
            sender = validator_set.choice_one()
            message = sender.create_message()
            sender.add_message(message)
            self.network.broadcast(message, sender)

        # Validators receive queued messages in every slot
        for receiver in validator_set.all():
            packets = self.network.receive(receiver)
            for packet in packets:
                receiver.add_message(packet.message)
        return self.network
