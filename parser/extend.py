from typing import List, Dict

import ast
from parser.exceptions import ExpandError

def expand_formals(nodes: List[ast.Node]) -> ast.Node:
    prev: ast.Pair = ast.Pair(None, None)
    curr: ast.Pair = ast.Pair(None, None)

    front: ast.Pair = prev
    dotted: bool = False

    exists: Dict[str, bool] = {}

    for i, node in enumerate(nodes):
        if isinstance(node, ast.Name):
            id = node.identifier
            if id == '.':
                dotted = True
                if i+1 == len(nodes):
                    raise ExpandError('unexpected \')\' after dot')
            else:
                if id in exists:
                    raise ExpandError(f'duplicate argument identifier: {node}')
                else:
                    exists[id] = True
                if dotted:
                    prev.second = node
                    if i+1 < len(nodes):
                        raise ExpandError('illegal use of \'.\'')
                else:
                    curr.first = node
                    prev.second = curr
                    prev = curr
                    curr = ast.Pair(None, None)
        else:
            raise ExpandError(f'illegal argument type: {node}')
    return front.second


def expand_list(nodes: List[ast.Node]) -> ast.Node:
    prev: ast.Pair = ast.Pair(None, None)
    curr: ast.Pair = ast.Pair(None, None)

    front: ast.Pair = prev
    dotted: bool = False
    for i, node in enumerate(nodes):
        is_dot: bool = False
        expanded: ast.Node = node
        if isinstance(node, ast.Name):
            id: str = node.identifier
            if id == '.':
                is_dot = True
                dotted = True
                if i == 0 or i+2 != len(nodes):
                    raise ExpandError('illegal use of \'.\'')
        elif isinstance(node, ast.Tuple):
            elements: List[ast.Node] = node.elements
            expanded = expand_list(elements)
        if not is_dot:
            if dotted:
                prev.second = expanded
            else:
                prev.second = curr
                curr.first = expanded
                prev = curr
                curr = ast.Pair(None, None)
    return front.second
