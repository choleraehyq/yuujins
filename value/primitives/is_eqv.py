from typing import List

from value import Value, PrimFunc, ArgsNotFit, Int, Float, Bool, String, Symbol, NULL_PAIR_VALUE
from value.primitives.typeof import TypeOf
class IsEqv(PrimFunc):

    def __init__(self) -> None:
        super(IsEqv, self).__init__('eqv?')

    def apply(self, args: List[Value]) -> Value:
        if len(args) != 2:
            raise ArgsNotFit(f'argument mismatch for \'eqv?\', expected 2, given: {len(args)}')
        type_of = TypeOf()
        symbol1, symbol2 = type_of.apply(args[0:1]), type_of.apply(args[1:2])
        if symbol1.val != symbol2.val:
            return Bool(False)
        is_eqv: Bool = False
        x, y = args[0], args[1]
        if isinstance(x, NULL_PAIR_VALUE):
            return Bool(True)
        if isinstance(x, Bool) or isinstance(x, Float) or isinstance(x, Int) or isinstance(x, String) or isinstance(x, Symbol):
            # Make PyCharm happy
            if isinstance(y, Bool) or isinstance(y, Float) or isinstance(y, Int) or isinstance(y, String) or isinstance(y, Symbol):
                is_eqv = x.val == y.val
        return Bool(is_eqv)