from __future__ import annotations
import yaml


class Config:
    def __init__(
        self,
        validator_num: int,
        max_slot: int = 50
    ):
        self.validator_num = validator_num
        self.max_slot = max_slot

    @classmethod
    def default(cls) -> Config:
        return Config(3, 50)

    @classmethod
    def from_yaml(cls, name) -> Config:
        with open(name) as f:
            obj = yaml.safe_load(f)
        return Config(
            obj['validator_num'],
            obj['max_slot']
        )
