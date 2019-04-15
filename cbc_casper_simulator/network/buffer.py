from cbc_casper_simulator.validator import Validator
from cbc_casper_simulator.network.packet import Packet
from typing import Dict, List


class Buffer:
    # FIXME: Rename
    def __init__(self):
        self.arrival_slot_to_packets: Dict[Validator, Dict[int, List[Packet]]] = dict()

    def add_packet_to_be_arrived(self, receiver: Validator, arrival_slot: int, packet: Packet):
        if receiver in self.arrival_slot_to_packets:
            packets = self.arrival_slot_to_packets[receiver].get(arrival_slot, []) + [packet]
            self.arrival_slot_to_packets[receiver][arrival_slot] = packets
        else:
            self.arrival_slot_to_packets[receiver] = {arrival_slot: [packet]}

    def read(self, receiver: Validator, slot: int) -> List[Packet]:
        # FIXME: Rename
        return self.arrival_slot_to_packets.get(receiver, dict()).get(slot, [])
