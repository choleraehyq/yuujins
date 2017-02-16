from typing import List, Optional

from value import Value, PrimFunc, ArgsNotFit

class Newline(PrimFunc):

    def __init__(self) -> None:
        super(Newline, self).__init__('newline')

    def apply(self, args: List[Value]) -> Optional[Value]:
        if len(args) != 0:
            raise ArgsNotFit('newline: argument mismatch, expected 0')
        print()