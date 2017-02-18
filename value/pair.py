from typing import Optional

from value.value import Value

class EmptyPair(Value):

    def __init__(self):
        self.first = None
        self.second = None

NULL_PAIR_VALUE = EmptyPair()

class Pair(Value):

    def __init__(self, first: Optional[Value], second: Optional[Value]) -> None:
        self.first: Optional[Value]
        self.second: Optional[Value]
        self.first, self.second = first, second
        if self.second is None:
            self.second = NULL_PAIR_VALUE

    def __str__(self) -> str:
        if self.first is None and self.second is None:
            return '()'
        if self.second is NULL_PAIR_VALUE:
            return '({})'.format(self.first)
