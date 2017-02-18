from typing import List

from ast import Node, Name
from scope import Scope
from value import Value
import binder

class LetRec(Node):

    def __init__(self, patterns: List[Name], exprs: List[Node], body: Node) -> None:
        self.patterns: List[Name] = patterns
        self.exprs: List[Node] = exprs
        self.body: Node = body

    def eval(self, s: Scope) -> Value:
        env: Scope = Scope(s)
        ext: List[Scope]
        for i in range(len(self.patterns)):
            ext.append(Scope(env))
            binder.define(ext[i], self.patterns[i].identifier, self.exprs[i].eval(env))
        for x in ext:
            env.put_all(x)
        return self.body.eval(env)

    def __str__(self) -> str:
        bindings: str = ' '.join(['({} {})'.format(self.patterns[i], self.exprs[i]) for i in range(len(self.patterns))])
        return f'(letrec ({bindings}) {self.body})'