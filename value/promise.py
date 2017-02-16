from value import Value

class Promise(Value):

    def __init__(self, env, lazy):
        self.is_val, self.env, self.lazy = True, env, lazy

    def __str__(self) -> str:
        return '#<promise>'