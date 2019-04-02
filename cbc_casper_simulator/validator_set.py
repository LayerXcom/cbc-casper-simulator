from __future__ import annotations
from typing import List
from cbc_casper_simulator.validator import Validator
import random as r


class ValidatorSet:
    def __init__(self, validators: List[Validator] = None):
        if validators is None:
            self.validators = []
        else:
            self.validators = validators

    def add(self, validator: Validator):
        self.validators.append(validator)

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
