from ast import Node
from value import Value, Int as IntValue
from scope import Scope


class Int(Node):

    def __init__(self, s: str) -> None:
        base: int = 10
        if s.startswith('0x') or s.startswith('0X'):
            base = 16
        elif s.startswith('0o') or s.startswith('0O'):
            base = 8
        self.val: int = int(s, base)
        self.base: int = base

    def eval(self, env: Scope) -> Value:
        return IntValue(self.val)

    def __str__(self) -> str:
        if self.base == 16:
            return '%x' % self.val
        elif self.base == 8:
            return '%o' % self.val
        else:
            return '%d' % self.val