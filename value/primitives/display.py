from typing import List, Optional

from value import Value, PrimFunc, ArgsNotFit

class Display(PrimFunc):

    def __init__(self) -> None:
        super(Display, self).__init__('display')

    def apply(self, args: List[Value]) -> Optional[Value]:
        if len(args) != 1:
            raise ArgsNotFit('display: argument mismatch, expected 1')
        print(args, end='')