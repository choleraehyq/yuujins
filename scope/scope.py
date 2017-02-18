from copy import deepcopy
from typing import Optional

from value import primitives, Bool


class Scope(object):

    def __init__(self, parent: Optional['Scope']) -> None:
        self.parent: Scope = parent
        self.env: dict = {}

    def put(self, name: str, value) -> None:
        self.env[name] = value

    def put_all(self, other: 'Scope') -> None:
        self.env = deepcopy(other.env)

    def look_up_local(self, name: str):
        return self.env.get(name)

    def look_up(self, name: str):
        val = self.look_up_local(name)
        if val is not None:
            return val
        elif self.parent is not None:
            return self.parent.look_up(name)
        else:
            return None

    def find_scope(self, name: str) -> Optional['Scope']:
        if self.look_up_local(name) is not None:
            return self
        elif self.parent is not None:
            return self.parent.find_scope(name)
        else:
            return None

def root_scope() -> Scope:
    root = Scope(None)
    root.put('+', primitives.Add())
    root.put('-', primitives.Sub())
    root.put('*', primitives.Mult())
    root.put('/', primitives.Div())
    root.put('=', primitives.Add())
    root.put('>', primitives.Gt())
    root.put('<', primitives.Lt())
    root.put('>=', primitives.GtE())
    root.put('<=', primitives.LtE())
    root.put('%', primitives.Mod())
    root.put('and', primitives.And())
    root.put('or', primitives.Or())
    root.put('eqv?', primitives.IsEqv())
    root.put('type-of', primitives.TypeOf())
    root.put('display', primitives.Display())
    root.put('newline', primitives.Newline())
    root.put('car', primitives.Car())
    root.put('cdr', primitives.Cdr())
    root.put('cons', primitives.Cons())
    root.put('sleep', primitives.Sleep())
    root.put('random', primitives.Random())
    root.put('#t', Bool(True))
    root.put('#f', Bool(False))
    return root
