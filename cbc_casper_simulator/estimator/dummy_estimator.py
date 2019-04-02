from cbc_casper_simulator.block import Block
from cbc_casper_simulator.state import State
from cbc_casper_simulator.justification import Justification


class DummyEstimator:
    @classmethod
    def estimate(cls, state: State, justification: Justification) -> Block:
        parent_hash = state.last_finalized_block.hash
        return Block(parent_hash)

    @classmethod
    def verify(cls, state: State, block: Block, justification: Justification) -> bool:
        return cls.estimate(state, justification) == block
