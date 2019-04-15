from __future__ import annotations
from typing import Iterator
from cbc_casper_simulator.validator_set import ValidatorSet
from cbc_casper_simulator.validator import Validator
from cbc_casper_simulator.network.model import Model as NetworkModel
from cbc_casper_simulator.util.ticker import Ticker
from cbc_casper_simulator.simulator.config import Config
from cbc_casper_simulator.block_proposer import BlockProposer


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
        self.broadcast_from_random_validator()
        self.all_validators_receive_all_packets()
        self.ticker.tick()
        return self.network

    def validator_rotation(self, i):
        # NOTE: Now, we assume the oldest validator exit for simplicity
        oldest_validator = self.network.validator_set.validators[0]
        self.network.exit(oldest_validator)
        new_validator = Validator("nv{}".format(i), 1.0, self.ticker)
        self.network.join(new_validator)

    def broadcast_from_random_validator(self):
        sender = BlockProposer.choose(self.ticker.current(), self.network.validator_set.validators)
        assert sender is not None, "no block proposer"
        message = sender.create_message()
        if message.estimate.is_checkpoint(self.config.checkpoint_interval):
            self.validator_rotation(self.ticker.current())
        message.estimate.active_validators = self.network.validator_set.validators
        res = sender.add_message(message)
        assert res.is_ok(), res.value
        self.network.broadcast(message, sender)

    def all_validators_receive_all_packets(self):
        for receiver in self.network.validator_set.all():
            packets = self.network.receive(receiver)
            for packet in packets:
                res = receiver.add_message(packet.message)
                assert res.is_ok(), "{} ({})".format(res.value, receiver.name)
