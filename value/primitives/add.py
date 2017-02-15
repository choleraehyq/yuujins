from typing import List

from value.value import Value
from value.primfunc import PrimFunc

class Add(PrimFunc):

    def __init__(self):
        self.name: str = '+'

    def apply(self, args: List[Value]) -> Value:
        # TODO(Cholerae): write real apply function
        return Value()