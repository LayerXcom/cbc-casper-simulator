from cbc_casper_simulator.block import Block
from cbc_casper_simulator.state import State
from cbc_casper_simulator.justification import Justification
from cbc_casper_simulator.weight import Weight
from cbc_casper_simulator.store import Store
from typing import Dict
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cbc_casper_simulator.validator import Validator


class LMDGhostEstimator:
    @classmethod
    def estimate(cls, state: State, justification: Justification) -> Block:
        scores: Dict[Block, float] = cls.score(state, justification)
        store = state.store

        best_block = store.last_finalized_block
        while store.has_children_blocks(best_block):
            best_block = max(store.children_blocks(
                best_block), key=lambda x: scores[x])
        return Block(best_block.hash)

    @classmethod
    def verify(cls, state: State, block: Block, justification: Justification) -> bool:
        return cls.estimate(state, justification) == block

    @classmethod
    def score(cls, state: State, justification: Justification) -> Dict[Block, float]:
        weights: Dict[Validator, float] = Weight.weights(state)
        scores: Dict[Block, float] = dict()
        store = state.store
        for v, m in justification.latest_messages.items():
            current_block = store.to_block(m)
            while not current_block.is_genesis():
                scores[current_block] = scores.get(
                    current_block, 0) + weights[v]
                current_block = store.parent_block(current_block)
        return scores
