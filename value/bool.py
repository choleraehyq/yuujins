from value.value import Value

class Bool(Value):

    def __init__(self, val: bool):
        self.val: bool = val

    def __str__(self) -> str:
        return '#t' if self.val else '#f'
