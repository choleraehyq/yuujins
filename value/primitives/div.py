from typing import List

from value import Value, PrimFunc, Int, Float, ArgsNotFit

class Div(PrimFunc):

    def __init__(self):
        super(Div, self).__init__('-')

    def apply(self, args: List[Value]) -> Value:
        val: float = 1
        if len(args) < 1:
            raise ArgsNotFit('\'/\' argument unmatch: expected at least 1')
        else:
            x = args[0]
            if isinstance(x, Int) or isinstance(x, Float):
                val = x.val
            else:
                raise ArgsNotFit(f'incorrect argument type for \'/\' : {x}')
            args = args[1:]
        if len(args) == 0 and val == 0:
            raise ArgsNotFit('\'/\': division by zero')
        for x in args:
            if x == 0:
                raise ArgsNotFit('\'/\': division by zero')
            if isinstance(x, Int) or isinstance(x, Float):
                val /= x.val
            else:
                raise ArgsNotFit(f'incorrect argument type for \'/\' : {x}')
        return Float(val)