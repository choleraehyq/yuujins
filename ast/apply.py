from typing import List

from ast import Node, eval_list, bind_arguments, Lambda
from value import Value, Closure, PrimFunc, ArgsNotFit, Pair as PairValue, NULL_PAIR_VALUE
from scope import Scope
from converter import pairs_to_slice


class Apply(Node):

    def __init__(self, proc: Node, args: List[Node]) -> None:
        self.proc: Node = proc
        self.args: List[Node] = args

    def eval(self, s: Scope) -> Value:
        proc: Value = self.proc.eval(s)
        args: Value = expand_apply_args(eval_list(self.args, s))
        if isinstance(proc, Closure):
            if not isinstance(proc.body, Lambda):
                raise TypeError(f'unexpected type: {proc.body}')
            bind_arguments(proc.env, proc.body.params, args)
            return proc.body.body.eval(proc.env)
        elif isinstance(proc, PrimFunc):
            return proc.apply(pairs_to_slice(args))
        else:
            raise ArgsNotFit(f'apply: expected a procedure, got {self.proc}')


    def __str__(self) -> str:
        return f'(apply {self.proc} {self.args})'


def expand_apply_args(args: List[Value]) -> Value:
    prev, curr = PairValue(None, None), PairValue(None, None)
    front = prev
    expect_list: bool = False

    for i, arg in enumerate(args):
        if isinstance(arg, PairValue):
            prev.second = arg
            while True:
                if isinstance(arg, PairValue):
                    arg = arg.second
                elif arg is NULL_PAIR_VALUE:
                    break
                else:
                    raise ArgsNotFit(f'apply: expected list, got {arg}')
            expect_list = False
            if i != len(args)-1:
                raise ArgsNotFit(f'apply: expected list, got {arg}')
        elif arg is NULL_PAIR_VALUE:
            expect_list = False
            if i != len(args)-1:
                raise ArgsNotFit(f'apply: expected list, got {arg}')
        else:
            expect_list = True
            curr.first = arg
            prev.second = curr
            prev = curr
            curr = PairValue(None, None)
    if expect_list:
        raise ArgsNotFit(f'apply: expected list, got {args[-1]}')
    return front.second
