from typing import List

from value import Value, PrimFunc, Bool, ArgsNotFit

class And(PrimFunc):

    def __init__(self) -> None:
        super(And, self).__init__('and')

    def apply(self, args: List[Value]) -> Value:
        ret: bool = True
        for x in args:
            if isinstance(x, Bool):
                ret = x.val and ret
            else:
                raise ArgsNotFit(f'incorrect argument type for \'and\': {x}, expected bool')
        return Bool(ret)