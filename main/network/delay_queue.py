from typing import List, Generic, Optional, TypeVar
T = TypeVar('T')


class DelayQueue(Generic[T]):
    def __init__(self):
        self.queue: List[(T, int)] = []

    def put(self, item: T, current_slot: int = 0):
        self.queue.append((item, current_slot))

    def get(self, current_slot: int = 0, delay: int = 0) -> Optional[T]:
        for index, item in enumerate(reversed(self.queue)):
            if item[1] <= current_slot - delay:
                del self.queue[len(self.queue) - index - 1]
                return item[0]
        return None

    def empty(self, current_slot: int = 0, delay: int = 0) -> bool:
        for item in self.queue:
            if item[1] <= current_slot - delay:
                return False
        return True
