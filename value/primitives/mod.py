from typing import List

from value import Value, PrimFunc, ArgsNotFit, Int

class Mod(PrimFunc):

    def __init__(self) -> None:
        super(Mod, self).__init__('%')

    def apply(self, args: List[Value]) -> Value:
        if len(args) != 2:
            raise ArgsNotFit(f'argument mismatch for \'%\', expected 2, given: {len(args)}')
        x, y = args[0], args[1]
        if isinstance(x, Int) and isinstance(y, Int):
            if y.val == 0:
                raise ArgsNotFit('remainder: undefined for 0')
            return Int(x.val % y.val)
        raise ArgsNotFit('incorrect argument type for \'%\', expected integer')
