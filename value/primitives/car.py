from typing import List

from value import Value, PrimFunc, ArgsNotFit, Pair

class Car(PrimFunc):

    def __init__(self) -> None:
        super(Car, self).__init__('car')

    def apply(self, args: List[Value]) -> Value:
        if len(args) != 1:
            raise ArgsNotFit(f'car: arguments mismatch, expected 1, given: {len(args)}')
        pairs = args[0]
        if not isinstance(pairs, Pair):
            raise ArgsNotFit(f'car: expected pair, given: {pairs}')
        return pairs.first