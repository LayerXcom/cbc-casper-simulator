from main.validator_set import ValidatorSet
from main.validator import Validator
from main.message import Message
from main.util.ticker import Ticker
from main.network.packet import Packet
from queue import Queue
from typing import Dict, List


class Model:
    def __init__(self, validator_set: ValidatorSet, ticker: Ticker = None):
        self.validator_set: ValidatorSet = validator_set
        self.queue: Dict[Validator, Queue] = dict()
        if ticker is None:
            self.ticker = Ticker()
        else:
            self.ticker = ticker

    def send(self, message: Message, sender: Validator, receiver: Validator):
        current_slot = self.ticker.current()
        packet = Packet(message, sender, receiver, current_slot)
        self.queue.setdefault(receiver, Queue())
        self.queue[receiver].put(packet)

    def receive(self, receiver: Validator) -> List[Packet]:
        packets = []
        self.queue.setdefault(receiver, Queue())
        while not self.queue[receiver].empty():
            packets.append(self.queue[receiver].get())
        return packets

    def broadcast(self, message: Message, sender: Validator):
        for receiver in self.validator_set.all():
            if sender != receiver:
                self.send(message, sender, receiver)
