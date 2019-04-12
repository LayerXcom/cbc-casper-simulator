from __future__ import annotations
from typing import List
from cbc_casper_simulator.validator import Validator
from cbc_casper_simulator.message import Message
import random as r


class ValidatorSet:
    def __init__(self, validators: List[Validator]):
        assert len(validators) > 0, "At least one validator is required."
        self.validators = validators
        self.genesis = Message.genesis(r.choice(self.validators), validators)

        # Add genesis message to all validators
        for validator in self.validators:
            res = validator.add_message(self.genesis)
            assert res.is_ok(), res.value

    def entry(self, new_validator: Validator, source_validator: Validator):
        # FIXME: move this to network layer
        assert new_validator not in self.validators, "{} already exists".format(new_validator.name)

        if new_validator.state.store.genesis is None:
            res = new_validator.add_message(self.genesis)
            assert res.is_ok(), res.value

        # FIXME: Do simulation of message arrival from the start for new validator
        for message in source_validator.state.store.messages.values():
            if message.is_genesis():
                continue
            res = new_validator.add_message(message)
            assert res.is_ok(), res.value

        self.validators.append(new_validator)

    def exit(self, validator: Validator):
        # FIXME: move this to network layer
        assert validator in self.validators, "{} does not exist".format(validator.name)
        self.validators.remove(validator)

    def choice(self, num=1) -> List[Validator]:
        population = min(num, len(self.validators))
        return r.sample(self.validators, population)

    def choice_one(self) -> Validator:
        return r.choice(self.validators)

    def all(self) -> List[Validator]:
        return self.validators

    def dump(self):
        return [validator.dump() for validator in self.all()]

    @classmethod
    def with_random_weight(cls, num, ticker) -> ValidatorSet:
        validators: List[Validator] = []
        for i in range(num):
            validators.append(Validator("v{}".format(i), r.random(), ticker))
        return ValidatorSet(validators)

    @classmethod
    def with_equal_weight(cls, num, ticker) -> ValidatorSet:
        validators: List[Validator] = []
        for i in range(num):
            validators.append(Validator("v{}".format(i), 1.0, ticker))
        return ValidatorSet(validators)
