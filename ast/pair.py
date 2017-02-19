from typing import Optional

from ast import Node, Name, UnquoteSplicing
from scope import Scope
from value import Value, NULL_PAIR_VALUE, Symbol, Pair as PairValue


class EmptyPair(Node):
    pass

NULL_PAIR = EmptyPair()


class Pair(Node):

    def __init__(self, first: Optional[Node], second: Optional[Node]) -> None:
        self.first: Node = first
        self.second: Node = second
        if self.second is None:
            self.second = NULL_PAIR

    def eval(self, env: Scope) -> Value:
        first: Value
        second: Value
        if self.second is NULL_PAIR:
            second = NULL_PAIR_VALUE
        else:
            if isinstance(self.second, Name):
                second = Symbol(self.second.identifier)
            else:
                second = self.second.eval(env)
        if isinstance(self.first, Name):
            first = Symbol(self.first.identifier)
        elif isinstance(self.first, UnquoteSplicing):
            first = self.first.eval(env)
            if first is NULL_PAIR_VALUE:
                return second
            last: Value = first
            while True:
                if isinstance(last, PairValue):
                    if last.second is NULL_PAIR_VALUE:
                        last.second = second
                        return first
                else:
                    if second is NULL_PAIR_VALUE:
                        return first
                    else:
                        raise TypeError(f'unquote-splicing: expected list, given {first}')
        else:
            first = self.first.eval(env)
        return PairValue(first, second)

    def __str__(self) -> str:
        if self.second is NULL_PAIR:
            return f'{self.first}'
        if isinstance(self.second, Pair):
            return f'({self.first} {str(self.second)[1:]}'
        else:
            return f'({self.first} . {self.second})'

