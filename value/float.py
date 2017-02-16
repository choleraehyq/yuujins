from value.value import Value

class Float(Value):

    def __init__(self, val: float) -> None:
        self.val: float = val

    def __str__(self) -> str:
        return repr(self.val)
