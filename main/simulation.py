from main.message import Message
from main.validator_set import ValidatorSet
from main.network.model import Model as NetworkModel
from main.util.ticker import Ticker


class SimulationConfig:
    def __init__(
        self,
        validator_num: int,
        network_latency: float = 0
    ):
        self.validator_num = validator_num
        self.network_latency = network_latency


class Simulation:
    def __init__(
            self,
            config: SimulationConfig = None
    ):
        if config is None:
            self.config = SimulationConfig(5)
        else:
            self.config = config

    def start(self):
        ticker = Ticker()
        validator_set = ValidatorSet.with_random_weight(self.config.validator_num, ticker)
        network = NetworkModel(validator_set, ticker)

        # genesis message
        genesis = Message.genesis(validator_set.choice_one())
        genesis.sender.add_message(genesis)
        network.broadcast(genesis, genesis.sender)
        for receiver in validator_set.all():
            packets = network.receive(receiver)
            for packet in packets:
                receiver.add_message(packet.message)
        ticker.tick()

        for i in range(10):
            sender = validator_set.choice_one()
            message = sender.create_message()
            sender.add_message(message)
            network.broadcast(message, sender)
            for receiver in validator_set.all():
                packets = network.receive(receiver)
                for packet in packets:
                    receiver.add_message(packet.message)
            ticker.tick()

        return validator_set
