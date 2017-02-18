from ast import Node, UndefinedIdentifier
from scope import Scope
from value import Value


class Name(Node):

    def __init__(self, identifier: str) -> None:
        self.identifier: str = identifier

    def eval(self, env: Scope) -> Value:
        val = env.look_up(self.identifier)
        if val is not None:
            return val
        raise UndefinedIdentifier(f'Undefined identifier: {self.identifier}')

    def __str__(self) -> str:
        return self.identifier
