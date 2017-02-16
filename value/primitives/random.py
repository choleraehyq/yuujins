from typing import List
import random

from value import Value, PrimFunc, ArgsNotFit, Int

class Random(PrimFunc):

    def __init__(self) -> None:
        super(Random, self).__init__('random')

    def apply(self, args: List[Value]) -> Value:
        if len(args) != 1:
            raise ArgsNotFit('random: argument mismatch, expected 1')
        random.seed()
        x = args[0]
        if not isinstance(x, Int):
            raise ArgsNotFit(f'random: expected integer, given: {x}')
        if x <= 0:
            raise ArgsNotFit(f'random: expected positive integer, given: {x}')
        return Int(random.randrange(0, x))