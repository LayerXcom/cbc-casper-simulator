from main.block import Block
from main.state import State
from main.justification import Justification


class DummyEstimator:
    @classmethod
    def estimate(cls, state: State, justification: Justification) -> Block:
        parent = state.last_finalized_block
        return Block(parent)

    @classmethod
    def verify(cls, state: State, block: Block) -> bool:
        return cls.estimate(state) == block
