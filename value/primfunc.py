from typing import List

from value.value import Value

class PrimFunc(Value):

    def __init__(self, name: str):
        self.name: str = name

    def __str__(self) -> str:
        return self.name

    def apply(self, args: List[Value]) -> Value:
        pass
