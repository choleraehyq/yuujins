from typing import List

from value import Value, PrimFunc, ArgsNotFit, Int, Float

class Mult(PrimFunc):

    def __init__(self) -> None:
        super(Mult, self).__init__('*')

    def apply(self, args: List[Value]) -> Value:
        val1: int = 1
        val2: float = 1
        is_float: bool = False
        for x in args:
            if isinstance(x, Int):
                val1 *= x.val
            elif isinstance(x, Float):
                is_float = True
                val2 *= x.val
            else:
                raise ArgsNotFit(f'incorrect argument type for \'*\' : {x}')
        if not is_float:
            return Int(val1)
        else:
            return Float(val1 * val2)