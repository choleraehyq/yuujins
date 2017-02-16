from typing import List

from value import Value, PrimFunc, ArgsNotFit, Int, Float, Bool, String, Pair, NULL_PAIR_VALUE, Closure, Symbol

class TypeOf(PrimFunc):

    def __init__(self) -> None:
        super(TypeOf, self).__init__('type-of')

    def apply(self, args: List[Value]) -> Symbol:
        if len(args) != 1:
            raise ArgsNotFit(f'argument mismatch for \`type-of\', expected 1, given: {len(args)}')

        symbol: str = 'unknown'
        x = args[0]
        if isinstance(x, Int):
            symbol = 'integer'
        elif isinstance(x, Float):
            symbol = 'float'
        elif isinstance(x, Bool):
            symbol = 'bool'
        elif isinstance(x, String):
            symbol = 'string'
        elif isinstance(x, NULL_PAIR_VALUE):
            symbol = 'nilpair'
        elif isinstance(x, Pair):
            symbol = 'pair'
        elif isinstance(x, Closure):
            symbol = 'procedure'
        elif isinstance(x, PrimFunc):
            symbol = 'procedure'
        elif isinstance(x, Symbol):
            symbol = x.val

        return Symbol(symbol)