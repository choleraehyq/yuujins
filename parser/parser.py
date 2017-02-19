from typing import List

from ast import Node
from lexer import Lexer
from parser import preparse, expand_list, expand_formals
from parser.exceptions import ParseError
import ast
import constants


def parse_node(node: Node) -> Node:
    if not isinstance(node, ast.Tuple):
        return node
    elements = node.elements
    if len(elements) == 0:
        raise ParseError('syntax error, empty list')
    elem = elements[0]
    if isinstance(elem, ast.Name):
        if elem.identifier == constants.DEFINE:
            return parse_define(node)
        elif elem.identifier == constants.BEGIN:
            return parse_begin(node)
        elif elem.identifier == constants.LAMBDA:
            return parse_lambda(node)
        elif elem.identifier == constants.LET or elem.identifier == constants.LET_REC or elem.identifier == constants.LET_STAR:
            return parse_let_family(node)
        elif elem.identifier == constants.IF:
            return parse_if(node)
        elif elem.identifier == constants.SET:
            return parse_set(node)
        elif elem.identifier == constants.APPLY:
            return parse_apply(node)
        elif elem.identifier == constants.QUOTE:
            return parse_quote(node)
        elif elem.identifier == constants.QUASIQUOTE:
            return parse_quasiquote(node, 1)
        elif elem.identifier == constants.UNQUOTE:
            raise ParseError('unquote: not in quasiquote')
        elif elem.identifier == constants.UNQUOTE_SPLICING:
            raise ParseError('unquote-splicing: not in quasiquote')
        elif elem.identifier == constants.DELAY:
            return parse_delay(node)
        elif elem.identifier == constants.FORCE:
            return parse_force(node)
        else:
            return parse_call(node)
    elif isinstance(elem, ast.Tuple):
        return parse_call(node)
    else:
        raise ParseError(f'{node}: not a procedure')


def parse_list(nodes: List[Node]) -> List[Node]:
    return [parse_node(node) for node in nodes]


def parse_block(tp: ast.Tuple) -> ast.Block:
    return ast.Block(parse_list(tp.elements))


def parse_begin(tp: ast.Tuple) -> ast.Begin:
    return ast.Begin(ast.Block(parse_list(tp.elements[1:])))


def parse_apply(tp: ast.Tuple) -> ast.Apply:
    if len(tp.elements) < 3:
        raise ParseError('apply: bad syntax (missing expressions), expected at least 3')
    return ast.Apply(parse_node(tp.elements[1]), parse_list(tp.elements[2:]))


def parse_let_family(tp: ast.Tuple) -> ast.Node:
    if len(tp.elements) < 3:
        raise ParseError(f'{tp.elements[0]}: bad syntax, no expression in body')
    elem = tp.elements[1]
    if not isinstance(elem, ast.Tuple):
        raise ParseError(f'{tp.elements[0]}: bad syntax, expected bindings, given: {elem}')
    bindings: List[Node] = elem.elements
    patterns: List[ast.Name] = []
    exprs: List[Node] = []
    for i, binding in enumerate(bindings):
        if isinstance(binding, ast.Tuple):
            if len(binding.elements) == 2:
                if isinstance(binding.elements[0], ast.Name):
                    patterns.append(binding.elements[0])
                    exprs.append(parse_node(binding.elements[1]))
                    continue
        raise ParseError(f'{tp.elements[0]}: bad syntax, not an identifer and expression for a binding {binding}')
    body = ast.Block(parse_list(tp.elements[2:]))
    name = tp.elements[0]
    if not isinstance(name, ast.Name):
        raise ParseError(f'expected a Name, given {name}')
    if name.identifier == constants.LET:
        return ast.Let(patterns, exprs, body)
    elif name.identifier == constants.LET_STAR:
        return ast.LetStar(patterns, exprs, body)
    elif name.identifier == constants.LET_REC:
        return ast.LetRec(patterns, exprs, body)
    else:
        raise ParseError(f'{tp.elements[0]}: should not be here')


def parse_quote(tp: ast.Tuple) -> ast.Quote:
    elements = tp.elements
    if len(elements) != 2:
        raise ParseError('quote: wrong number of parts')
    elem = elements[1]
    if isinstance(elem, ast.Tuple):
        return ast.Quote(expand_list(elem.elements))
    else:
        return ast.Quote(elem)


def parse_unquote(tp: ast.Tuple, level: int) -> ast.Node:
    elements = tp.elements
    if len(elements) != 2:
        raise ParseError('unquote: wrong number of parts')
    if level == 0:
        return ast.Unquote(parse_node(elements[1]))
    else:
        elem = elements[1]
        if isinstance(elem, ast.Tuple):
            elements[1] = parse_nested_quasiquote(elem, level)
        return tp


def parse_unquote_splicing(tp: ast.Tuple, level: int) -> ast.Node:
    elements = tp.elements
    if len(elements) != 2:
        raise ParseError('unquote-splicing: wrong number of parts')
    if level == 0:
        return ast.UnquoteSplicing(parse_node(elements[1]))
    else:
        elem = elements[1]
        if isinstance(elem, ast.Tuple):
            elements[1] = parse_nested_quasiquote(elements[1], level)
        return tp


def parse_nested_quasiquote(tp: ast.Tuple, level: int) -> ast.Node:
    elements = tp.elements
    if len(elements) == 0:
        return tp
    name = elements[0]
    if isinstance(name, ast.Name):
        if name.identifier == constants.UNQUOTE:
            return parse_unquote(tp, level-1)
        elif name.identifier == constants.UNQUOTE_SPLICING:
            return parse_unquote_splicing(tp, level-1)
        elif name.identifier == constants.QUASIQUOTE:
            return parse_quasiquote(tp, level+1)
    slice: List[Node] = []
    for node in elements:
        if isinstance(node, ast.Tuple):
            node = parse_nested_quasiquote(node, level)
        slice.append(node)
    return ast.Tuple(slice)


def parse_quasiquote(tp: ast.Tuple, level: int) -> ast.Node:
    elements = tp.elements
    if len(elements) != 2:
        raise ParseError('quasiquote: wrong number of parts')
    elem = elements[1]
    if isinstance(elem, ast.Tuple):
        node = parse_nested_quasiquote(elem, level)
        if level > 1:
            elements[1] = node
            return tp
        else:
            if isinstance(node, ast.Tuple):
                return ast.Quasiquote(expand_list(node.elements))
            else:
                return ast.Quasiquote(node)
    else:
        return ast.Quasiquote(elements[1])


def parse_function(tp: ast.Tuple, tail: Node) -> ast.Function:
    lmd = ast.Lambda(None, tail)
    while True:
        elements = tp.elements
        lmd.params = expand_formals(elements[1:])
        if isinstance(elements[0], ast.Name):
            return ast.Function(elements[0], lmd)
        elif isinstance(elements[0], ast.Tuple):
            tp = elements[0]
            lmd = ast.Lambda(None, lmd)
        else:
            raise ParseError(f'Unsupported ast node type {elements[0]}')


def parse_define(tp: ast.Tuple) -> ast.Define:
    elements = tp.elements
    if len(elements) < 3:
        raise ParseError(f'define: bad syntax (missing expressions) {tp}')
    if isinstance(elements[1], ast.Name):
        if len(elements) > 3:
            raise ParseError(f'define: bad syntax (multiple expressions) {tp}')
        return ast.Define(elements[1], parse_node(elements[2]))
    elif isinstance(elements[1], ast.Tuple):
        tail = ast.Block(parse_list(elements[2:]))
        function = parse_function(elements[1], tail)
        return ast.Define(function.caller, function)
    else:
        raise ParseError(f'Unsupported ast node type: {elements[1]}')


def parse_call(tp: ast.Tuple) -> ast.Call:
    elements = tp.elements
    if len(elements) == 0:
        raise ParseError('missing procedure expression')
    callee = parse_node(elements[0])
    args = parse_list(elements[1:])
    return ast.Call(callee, args)


def parse_lambda(tp: ast.Tuple) -> ast.Lambda:
    elements = tp.elements
    if len(elements) < 3:
        raise ParseError(f'lambda: bad syntax: {tp}')
    pattern = elements[1]
    body = ast.Block(parse_list(elements[2:]))
    if isinstance(pattern, ast.Name):
        return ast.Lambda(pattern, body)
    elif isinstance(pattern, ast.Tuple):
        formals = expand_formals(pattern.elements)
        if isinstance(formals, ast.Pair) or formals is ast.NULL_PAIR:
            return ast.Lambda(formals, body)
        else:
            raise ParseError('lambda: illegal use of \'.\'')
    else:
        raise ParseError(f'Unsupported ast node type: {pattern}')


def parse_if(tp: ast.Tuple) -> ast.If:
    elements = tp.elements
    if len(elements) != 3 and len(elements) != 4:
        raise ParseError(f'incorrect format of if: {tp}')
    test = parse_node(elements[1])
    then = parse_node(elements[2])
    if len(elements) == 3:
        return ast.If(test, then, None)
    else:
        return ast.If(test, then, parse_node(elements[3]))


def parse_set(tp: ast.Tuple) -> ast.Set:
    elements = tp.elements
    if len(elements) != 3:
        raise ParseError(f'incorrect format of set!: {tp}')
    pattern = parse_node(elements[1])
    if not isinstance(pattern, ast.Name):
        raise ParseError(f'set!: not an identifier in {tp}')
    value = parse_node(elements[2])
    return ast.Set(pattern, value)


def parse_delay(tp: ast.Tuple) -> ast.Delay:
    elements = tp.elements
    if len(elements) != 2:
        raise ParseError(f'delay: bad syntax in: {tp}')
    return ast.Delay(parse_node(elements[1]))


def parse_force(tp: ast.Tuple) -> ast.Force:
    elements = tp.elements
    if len(elements) != 2:
        raise ParseError('force: argument number mismatch, expected 1')
    return ast.Force(parse_node(elements[1]))


def parse(l: Lexer) -> List[Node]:
    elements = preparse(l, ' ')
    return parse_list(elements)


def parse_from_string(name: str, program: str) -> List[Node]:
    return parse(Lexer(name, program))
