from main.message import Message
from main.validator_set import ValidatorSet
from main.network.model import Model as NetworkModel
from main.util.ticker import Ticker


class SimulatorConfig:
    def __init__(
        self,
        validator_num: int,
        network_latency: float = 0
    ):
        self.validator_num = validator_num
        self.network_latency = network_latency


class Simulator:
    def __init__(
            self,
            config: SimulatorConfig = None
    ):
        if config is None:
            self.config = SimulatorConfig(3)
        else:
            self.config = config

    def start(self):
        ticker = Ticker()
        validator_set = ValidatorSet.with_random_weight(
            self.config.validator_num, ticker)
        network = NetworkModel(validator_set, ticker)

        # genesis message
        genesis = Message.genesis(validator_set.choice_one())
        for validator in validator_set.all():
            validator.add_message(genesis)
        ticker.tick()

        for i in range(100):
            if i % 10 == 0:
                sender = validator_set.choice_one()
                message = sender.create_message()
                sender.add_message(message)
                network.broadcast(message, sender)

            self.all_receive(network, validator_set)
            ticker.tick()
        return validator_set

    def all_receive(self, network: NetworkModel, validator_set: ValidatorSet):
        for receiver in validator_set.all():
            packets = network.receive(receiver)
            for packet in packets:
                receiver.add_message(packet.message)
