from value import Value

class Symbol(Value):

    def __init__(self, val: str) -> None:
        self.val: str = val

    def __str__(self) -> str:
        return self.val
