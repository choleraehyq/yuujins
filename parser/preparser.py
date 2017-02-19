from typing import List

from lexer import Lexer, Token, TokenType
from ast import Node
import ast
import constants

from parser.exceptions import PreparseError


def preparse(l: Lexer, delimiter: str) -> List[Node]:
    token: Token = l.next_token()
    elements: List[Node] = []
    while token.ty != TokenType.TokenEOF:
        if token.ty == TokenType.TokenIdentifier:
            elements.append(ast.Name(token.val))
        elif token.ty == TokenType.TokenIntegerLiteral:
            elements.append(ast.Int(token.val))
        elif token.ty == TokenType.TokenFloatLiteral:
            elements.append(ast.Float(token.val))
        elif token.ty == TokenType.TokenStringLiteral:
            elements.append(ast.String(token.val))
        elif token.ty == TokenType.TokenOpenParen:
            tuple = ast.Tuple(preparse(l, '('))
            elements.append(tuple)
        elif token.ty == TokenType.TokenCloseParen:
            if delimiter != '(':
                raise PreparseError('read: unexpected \')\'')
            return elements
        elif token.ty == TokenType.TokenQuote:
            quote: List[Node] = [ast.Name(constants.QUOTE)]
            quote += preparse(l, '\'')
            elements.append(ast.Tuple(quote))
        elif token.ty == TokenType.TokenQuasiquote:
            quasiquote: List[Node] = [ast.Name(constants.QUASIQUOTE)]
            quasiquote += preparse(l, '`')
            elements.append(ast.Tuple(quasiquote))
        elif token.ty == TokenType.TokenUnquote:
            unquote: List[Node] = [ast.Name(constants.UNQUOTE)]
            unquote += preparse(l, ',')
            elements.append(ast.Tuple(unquote))
        elif token.ty == TokenType.TokenUnquoteSplicing:
            unquote_splicing: List[Node] = [ast.Name(constants.UNQUOTE_SPLICING)]
            unquote_splicing += preparse(l, ',@')
            elements.append(ast.Tuple(unquote_splicing))
        elif token.ty == TokenType.TokenError:
            raise PreparseError(f'token error: {token.val}')
        else:
            raise PreparseError(f'unexpected token type: {token.ty}')
        if delimiter in ('\'', '`', ',', ',@'):
            return elements
        token = l.next_token()
    if delimiter != ' ':
        raise PreparseError(f'unclosed delimiter, expected: \'{delimiter}\'')
    return elements