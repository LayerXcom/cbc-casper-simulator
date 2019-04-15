from typing import List, Optional
from cbc_casper_simulator.validator import Validator
from cbc_casper_simulator.util.sha256 import SHA256
import random as r


class BlockProposer:
    @classmethod
    def choose(cls, slot: int, validators: List[Validator]) -> Optional[Validator]:
        for validator in validators:
            active_validators = validator.head().active_validators
            # Global random oracle for block proposer election
            # We can get the same block proposer if slot and validators are same
            r.seed(cls.gen_hash(slot, active_validators))
            proposer_index = r.randint(0, len(active_validators) - 1)
            proposer = active_validators[proposer_index]
            if proposer == validator:
                return proposer
        return None

    @classmethod
    def gen_hash(cls, slot: int, validators: List[Validator]) -> int:
        sorted_validators = sorted(validators, key=lambda validator: validator.hash)
        text = str(slot) + " " + ''.join([str(validator.hash) for validator in sorted_validators])
        return int.from_bytes(SHA256.digest(text), byteorder='little')
