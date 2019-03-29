from __future__ import annotations
from typing import Dict, List, Optional
from main.message import Message
from main.block import Block
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main.validator import Validator


class Store:
    def __init__(self):
        self.message_history: Dict[Validator, List[int]] = dict()
        self.messages: Dict[int, Message] = dict()
        self.children: Dict[int, List[int]] = dict()
        self.parent: Dict[int, int] = dict()
        self.block_to_message_in_hash: Dict[int, int] = dict()
        self.genesis: Optional[Message] = None

    def add(self, message):
        self.block_to_message_in_hash[message.estimate.hash] = message.hash

        if message.hash not in self.messages:
            self.messages[message.hash] = message
        if message.sender not in self.message_history:
            self.message_history[message.sender] = []
        self.message_history[message.sender].append(message.hash)

        if message.is_genesis():
            self.genesis = message
        else:
            parent_message_hash = self.block_to_message_in_hash[message.estimate.parent_hash]
            self.parent[message.hash] = parent_message_hash
            if parent_message_hash not in self.children:
                self.children[parent_message_hash] = []
            self.children[parent_message_hash].append(message.hash)

    def get(self, message_hash: int) -> Optional[Message]:
        if message_hash not in self.messages:
            return None
        else:
            return self.messages[message_hash]

    def get_parent(self, message_hash: int) -> Optional[Message]:
        if message_hash not in self.parent:
            return None
        else:
            return self.parent[message_hash]

    def latest_messages(self) -> Dict['Validator', int]:
        return {v: l[-1] for (v, l) in self.message_history.items()}

    def block_chain(self) -> BlockStore:
        return BlockStore(self)

    def dump(self, state=None):
        return [m.dump(state, self.get(self.get_parent(m.hash))) for m in self.messages.values()]


class BlockStore:
    def __init__(self, message_store: Store):
        self.genesis: Block = message_store.genesis.estimate
        self.children: Dict[Block, List[Block]] = dict()
        self.parent: Dict[Block, Block] = dict()
        for (parent_hash, children_hashes) in message_store.children.items():
            parent = message_store.messages[parent_hash].estimate
            for child_hash in children_hashes:
                child = message_store.messages[child_hash].estimate
                if parent not in self.children:
                    self.children[parent] = []
                self.children[parent].append(child)
                self.parent[child] = parent

    def has_children(self, block: Block) -> bool:
        return len(self.get_children(block)) != 0

    def get_children(self, block: Block) -> List[Block]:
        if block not in self.children:
            return []
        else:
            return self.children[block]

    def get_parent(self, block: Block) -> Optional[Block]:
        if block.is_genesis():
            return None
        else:
            return self.parent[block]
