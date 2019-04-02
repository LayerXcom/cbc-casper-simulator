from cbc_casper_simulator.validator_set import ValidatorSet
from cbc_casper_simulator.validator import Validator
from cbc_casper_simulator.message import Message
from cbc_casper_simulator.util.ticker import Ticker
from cbc_casper_simulator.network.packet import Packet
from cbc_casper_simulator.network.delay_queue import DelayQueue
from cbc_casper_simulator.network.delay import RandomDelay as Delay
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
