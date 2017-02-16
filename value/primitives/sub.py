from typing import List

from value import Value, PrimFunc, Int, Float, ArgsNotFit

class Sub(PrimFunc):

    def __init__(self):
        super(Sub, self).__init__('-')

    def apply(self, args: List[Value]) -> Value:
        val: float
        is_float: bool = False
        if len(args) <= 1:
            raise ArgsNotFit('\'-\' argument unmatch: expected at least 2')
        elif len(args) > 1:
            x = args[0]
            if isinstance(x, Int) or isinstance(x, Float):
                val = x.val
                if isinstance(x, Float):
                    is_float = True
            else:
                raise ArgsNotFit(f'incorrect argument type for \'-\' : {x}')
            args = args[1:]
        for x in args:
            if isinstance(x, Int):
                val -= x.val
            if isinstance(x, Float):
                val -= x.val
                is_float = True
            else:
                raise ArgsNotFit(f'incorrect argument type for \'-\' : {x}')
        if not is_float:
            return Int(int(val))
        else:
            return Float(val)