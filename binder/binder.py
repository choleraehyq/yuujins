from scope import Scope
from value import Value

class NameNotDefined(Exception):

    def __init__(self, message: str):
        super(NameNotDefined, self).__init__(message)


def define(env: Scope, pattern: str, value: Value) -> None:
    env.put(pattern, value)


def assign(s: Scope, pattern: str, value: Value) -> None:
    env: Scope = s.find_scope(pattern)
    if env is not None:
        env.put(pattern, value)
    else:
        raise NameNotDefined('{} was not defined'.format(pattern))