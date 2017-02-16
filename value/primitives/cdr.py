from typing import List

from value import Value, PrimFunc, ArgsNotFit, Pair

class Cdr(PrimFunc):

    def __init__(self) -> None:
        super(Cdr, self).__init__('cdr')

    def apply(self, args: List[Value]) -> Value:
        if len(args) != 1:
            raise ArgsNotFit(f'cdr: arguments mismatch, expected 1, given: {len(args)}')
        pairs = args[0]
        if not isinstance(pairs, Pair):
            raise ArgsNotFit(f'cdr: expected pair, given: {pairs}')
        return pairs.second