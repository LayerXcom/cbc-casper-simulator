from __future__ import annotations


class SimulatorConfig:
    def __init__(
        self,
        validator_num: int,
        max_slot: int = 100
    ):
        self.validator_num = validator_num
        self.max_slot = max_slot

    @classmethod
    def default(cls) -> SimulatorConfig:
        return SimulatorConfig(3)
