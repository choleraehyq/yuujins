from copy import deepcopy
from typing import Optional

class Scope(object):
    def __init__(self, parent: Optional['Scope']) -> None:
        self.parent: Scope = parent
        self.env: dict = {}

    def put(self, name: str, value) -> None:
        self.env[name] = value

    def put_all(self, other) -> None:
        self.env = copy.deepcopy(other.env)

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

    def find_scope(self, name: str) -> typing.Optional['Scope']:
        if self.look_up_local(name) is not None:
            return self
        elif self.parent is not None:
            return self.parent.find_scope(name)
        else:
            return None

def root_scope() -> Scope:
    root = Scope(None)
    # TODO(Cholerae): Put primitives and bool values in root scope
    return root
