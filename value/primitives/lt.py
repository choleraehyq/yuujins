from typing import List

from value import Value, PrimFunc, ArgsNotFit, Int, Float, Bool

class Lt(PrimFunc):

    def __init__(self) -> None:
        super(Lt, self).__init__('<')

    def apply(self, args: List[Value]) -> Value:
        if len(args) != 2:
            raise ArgsNotFit(f'argument mismatch for \'<\', expected 2, given: {len(args)}')
        x, y = args[0], args[1]
        if (isinstance(x, Int) or isinstance(x, Float)) and (isinstance(y, Int) or isinstance(y, Float)):
            return Bool(x.val < y.val)
        raise ArgsNotFit('incorrect argument type for \'<\', expected number')