from typing import List

from value import Value
from value import PrimFunc
from value import Int, Float, ArgsNotFit

class Add(PrimFunc):

    def __init__(self):
        super(Add, self).__init__('+')

    def apply(self, args: List[Value]) -> Value:
        if len(args) <= 1:
            raise ArgsNotFit('\'+\' argument unmatch: expected at least 2')
        val1: int
        val2: float
        is_float: bool = False
        for x in args:
            if isinstance(x, Int):
                val1 += x.val
            elif isinstance(x, Float):
                is_float = True
                val2 += x.val
            else:
                raise ArgsNotFit(f'incorrect argument type for \'+\': {x}')
        if not is_float:
            return Int(val1)
        else:
            return Float(val1 + val2)