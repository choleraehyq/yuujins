from typing import List, Optional

from scope import Scope
from value import Value
from parser import parse_from_string
from ast import Node, eval_list

def REPL(exprs: str, env: Scope) -> str:
    result: str = ''
    first: bool = True

    sexprs: List[Node] = parser.parse_from_string('<REPL>', exprs)
    values: List[Optional[Value]] = ast.eval_list(sexprs, env)

    for val in values:
        if val is not None:
            if first:
                first = False
                result += str(val)
            else:
                result += '\n' + str(val)

    return result
