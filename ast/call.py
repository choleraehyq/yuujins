from typing import List

from ast import Node, eval_list, Lambda, Name, NULL_PAIR, Pair
from value import Value, Closure, PrimFunc, NULL_PAIR_VALUE, ArgsNotFit, Pair as PairValue
from scope import Scope
from converter import slice_to_pair_values


class Call(Node):

    def __init__(self, callee: Node, args: List[Node]) -> None:
        self.callee: Node = callee
        self.args: List[Node] = args

    def eval(self, s: Scope) -> Value:
        callee: Node = self.callee.eval(s)
        args = eval_list(self.args, s)
        if isinstance(callee, Closure):
            env: Scope = Scope(callee.env)
            if not isinstance(callee.body, Lambda):
                raise TypeError(f'unexpected type: {callee.body}')
            bind_arguments(env, callee.body.params, slice_to_pair_values(args))
            return callee.body.body.eval(env)
        elif isinstance(callee, PrimFunc):
            return callee.apply(args)
        else:
            raise TypeError(f'{callee}: not allowed in a call context, args: {self.args[0]}')

    def __str__(self) -> str:
        return '{} {}'.format(self.callee, ' '.join([str(x) for x in self.args]))


def bind_arguments(env: Scope, params: Node, args: Value) -> None:
    if isinstance(params, Name) and args is NULL_PAIR_VALUE:
        env.put(params.identifier, args)
        return
    while True:
        if params is NULL_PAIR and args is NULL_PAIR_VALUE:
            return
        elif params is NULL_PAIR and args is not NULL_PAIR_VALUE:
            raise ArgsNotFit('too many arguments')
        elif params is not NULL_PAIR and args is NULL_PAIR_VALUE:
            raise ArgsNotFit('missing arguments')
        if isinstance(params, Pair):
            name: Name = params.first
            if not isinstance(args, PairValue):
                raise ArgsNotFit('arguments does not match given number')
            env.put(name.identifier, args.first)
            params = params.second
        elif isinstance(params, Name):
            env.put(params.identifier, args)
            return