from typing import List, Optional
from time import sleep

from value import Value, PrimFunc, ArgsNotFit, Int
import constants

class Sleep(PrimFunc):

    def __init__(self) -> None:
        super(Sleep, self).__init__(constants.SLEEP)

    def apply(self, args: List[Value]) -> Optional[Value]:
        if len(args) != 1:
            raise ArgsNotFit('sleep : arguments mismatch, expected 1')
        x = args[0]
        if isinstance(x, Int):
            sleep(x.val * 0.001)
        else:
            raise ArgsNotFit('incorrect argument type for sleep')
