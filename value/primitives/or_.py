from typing import List

from value import Value, PrimFunc, ArgsNotFit, Bool

class Or(PrimFunc):

    def __init__(self) -> None:
        super(Or, self).__init__('or')

    def apply(self, args: List[Value]) -> Value:
        ret: bool = False
        for x in args:
            if isinstance(x, Bool):
                ret = ret or x.val
            else:
                raise ArgsNotFit('incorrect argument type for \`or\', expected bool')
        return Bool(ret)