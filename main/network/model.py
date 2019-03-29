from main.validator_set import ValidatorSet
from main.validator import Validator
from main.message import Message
from main.util.ticker import Ticker
from main.network.packet import Packet
from main.network.delay_queue import DelayQueue
from main.network.delay import RandomDelay as Delay
from typing import Dict, List


class Model:
    def __init__(self, validator_set: ValidatorSet, ticker: Ticker = None):
        self.validator_set: ValidatorSet = validator_set
        self.queue: Dict[Validator, DelayQueue] = dict()
        if ticker is None:
            self.ticker = Ticker()
        else:
            self.ticker = ticker

    def send(self, message: Message, sender: Validator, receiver: Validator):
        current_slot = self.ticker.current()
        packet = Packet(message, sender, receiver, current_slot)
        self.queue.setdefault(receiver, DelayQueue())
        self.queue[receiver].put(packet, packet.slot)

    def receive(self, receiver: Validator) -> List[Packet]:
        packets = []
        self.queue.setdefault(receiver, DelayQueue())
        delay = Delay.get(1, 9)
        while not self.queue[receiver].empty(self.ticker.current(), delay):
            packets.append(self.queue[receiver].get(self.ticker.current(), delay))
        return packets

    def broadcast(self, message: Message, sender: Validator):
        for receiver in self.validator_set.all():
            if sender != receiver:
                self.send(message, sender, receiver)
