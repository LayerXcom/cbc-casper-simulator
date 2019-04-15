from cbc_casper_simulator.validator_set import ValidatorSet
from cbc_casper_simulator.validator import Validator
from cbc_casper_simulator.message import Message
from cbc_casper_simulator.util.ticker import Ticker
from cbc_casper_simulator.network.packet import Packet
from cbc_casper_simulator.network.buffer import Buffer
from typing import List
import random as r

DELAY_MIN = 0
DELAY_MAX = 3


class Model:
    def __init__(self, validator_set: ValidatorSet, ticker: Ticker = None):
        self.validator_set: ValidatorSet = validator_set
        self.buffer: Buffer = Buffer()
        if ticker is None:
            self.ticker = Ticker()
        else:
            self.ticker = ticker

    def send(self, message: Message, sender: Validator, receiver: Validator):
        current_slot = self.ticker.current()
        packet = Packet(message, sender, receiver, current_slot)
        # FIXME: Decide delay w.r.t. network topology
        arrival_slot = packet.slot + r.randint(DELAY_MIN, DELAY_MAX)
        self.buffer.add_packet_to_be_arrived(receiver, arrival_slot, packet)

    def receive(self, receiver: Validator) -> List[Packet]:
        to_be_received: List[Packet] = []
        packets = self.buffer.read(receiver, self.ticker.current())
        for packet in packets:
            if receiver.message_is_to_be_pending(packet.message):
                self.buffer.add_packet_to_be_arrived(receiver, self.ticker.current() + 1, packet)
            else:
                to_be_received.append(packet)
        return to_be_received

    def broadcast(self, message: Message, sender: Validator):
        for receiver in self.validator_set.all():
            if sender != receiver:
                self.send(message, sender, receiver)

    def dump(self):
        return {
            "validators": self.validator_set.dump(),
            "slot": self.ticker.current()
        }
