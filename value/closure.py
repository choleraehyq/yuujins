from value import Value

class Closure(Value):

    def __init__(self, env, body):
        self.env, self.body = env, body

    def __str__(self) -> str:
        return '#<procedure>'