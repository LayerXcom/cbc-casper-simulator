from typing import List
from main.validator import Validator
import random as r


class ValidatorStore:
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

    def all(self) -> List[Validator]:
        return self.validators
