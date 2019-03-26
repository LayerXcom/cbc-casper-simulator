from main.block import Block
from main.state import State
from main.justification import Justification
from main.weight import Weight
from main.store.message_store import BlockStore
from typing import Dict
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main.validator import Validator


class LMDGhostEstimator:
    @classmethod
    def estimate(cls, state: State, justification: Justification) -> Block:
        chain: BlockStore = state.message_store.block_chain()
        scores: Dict[Block, float] = cls.score(state, justification)

        best_block = state.last_finalized_block
        while chain.has_children(best_block):
            best_block = max(chain.get_children(best_block), key=lambda x: scores[x])
        return Block(best_block.hash)

    @classmethod
    def verify(cls, state: State, block: Block) -> bool:
        return cls.estimate(state) == block

    @classmethod
    def score(cls, state: State, justification: Justification) -> Dict[Block, float]:
        weights: Dict[Validator, float] = Weight.weights(state)
        scores: Dict[Block, float] = dict()
        chain: BlockStore = state.message_store.block_chain()
        for v, m in justification.latest_messages.items():
            current_block = state.message_store.get(m).estimate
            while not current_block.is_genesis():
                scores[current_block] = scores.get(current_block, 0) + weights[v]
                current_block = chain.get_parent(current_block)
        return scores
