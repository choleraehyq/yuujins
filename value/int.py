from value.value import Value

class Int(Value):

    def __init__(self, v: int):
        self.val: int = v

    def __str__(self) -> str:
        return str(self.val)