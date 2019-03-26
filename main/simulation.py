from main.message import Message
from main.validator import Validator
from main.store.validator_store import ValidatorStore
from main.store.message_store import MessageStore
from main.ticker import Ticker


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
            self.config = SimulationConfig(2)
        else:
            self.config = config

        self.message_store = MessageStore()

    def start(self):
        ticker = Ticker()
        validator_store = ValidatorStore()
        for i in range(1, 3):
            validator_store.add(Validator("v{}".format(i), float(i), ticker))

        # genesis message
        genesis = Message.genesis(validator_store.choice()[0])
        for v in validator_store.all():
            v.state_transition(genesis)
            self.message_store.add(genesis)
        ticker.tick()

        sender, receiver = validator_store.choice(2)
        for i in range(100):
            self.create_and_send_message(sender, receiver)
            sender, receiver = receiver, sender
            ticker.tick()

        return validator_store

    def create_and_send_message(self, sender: Validator, receiver: Validator):
        message = sender.create_message()
        sender.state_transition(message)
        self.message_store.add(message)
        receiver.state_transition(message)
