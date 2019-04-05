from __future__ import annotations
from typing import Iterator
from cbc_casper_simulator.validator_set import ValidatorSet
from cbc_casper_simulator.network.model import Model as NetworkModel
from cbc_casper_simulator.util.ticker import Ticker
from cbc_casper_simulator.simulator.config import Config


class BroadCastAndReceiveSimulator(Iterator[NetworkModel]):
    def __init__(self,
                 config: Config
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
        if i > self.config.max_slot:
            raise StopIteration
        if i % 2 == 0:
            self.broadcast_from_random_validator()
        self.all_validators_receive_all_packets()
        self.ticker.tick()
        return self.network

    def broadcast_from_random_validator(self):
        sender = self.network.validator_set.choice_one()
        message = sender.create_message()
        res = sender.add_message(message)
        assert res.is_ok(), res.value
        self.network.broadcast(message, sender)

    def all_validators_receive_all_packets(self):
        for receiver in self.network.validator_set.all():
            packets = self.network.receive(receiver)
            for packet in packets:
                res = receiver.add_message(packet.message)
                assert res.is_ok(), res.value
