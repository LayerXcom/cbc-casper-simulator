from __future__ import annotations
from typing import Iterable
from cbc_casper_simulator.message import Message
from cbc_casper_simulator.validator_set import ValidatorSet
from cbc_casper_simulator.network.model import Model as NetworkModel
from cbc_casper_simulator.util.ticker import Ticker
from cbc_casper_simulator.simulator.simulator_config import SimulatorConfig


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
            current = self.network
        elif i > self.config.max_slot:
            raise StopIteration
        else:
            current = self.step()
        self.ticker.tick()
        return current

    def step(self) -> NetworkModel:
        validator_set = self.network.validator_set
        if self.ticker.current() % 2 == 0:
            # The validator randomly selected create and broadcast a message to other validators
            sender = validator_set.choice_one()
            message = sender.create_message()
            res = sender.add_message(message)
            assert res.is_ok(), res.value
            self.network.broadcast(message, sender)

        # Validators receive queued messages in every slot
        for receiver in validator_set.all():
            packets = self.network.receive(receiver)
            for packet in packets:
                res = receiver.add_message(packet.message)
                assert res.is_ok(), res.value

        return self.network
