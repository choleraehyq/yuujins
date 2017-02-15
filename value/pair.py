from typing import Optional

from value.value import Value

class Pair(Value):

    def __init__(self, first: Optional[Value], second: Optional[Value]):
        self.first: Optional[Value]
        self.second: Optional[Value]
        self.first, self.second = first, second


    def __str__(self) -> str:
        if self.first is None and self.second is None:
            return '()'
        if self.second is None:
            return '({})'.format(self.first)


