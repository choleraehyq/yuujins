from typing import List

from value import Value, PrimFunc, ArgsNotFit, Pair

class Cons(PrimFunc):

    def __init__(self) -> None:
        super(Cons, self).__init__('cons')

    def apply(self, args: List[Value]) -> Value:
        if len(args) != 2:
            raise ArgsNotFit(f'cons: arguments mismatch, expected 2, given: {len(args)}')
        return Pair(args[0], args[1])