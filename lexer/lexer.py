from typing import Optional, Callable

from lexer import Token, TokenType

class Lexer(object):

    def __init__(self, name: str, input: str):
        self.name: str = name
        self.input: str = input
        self.pos: int = 0
        self.start: int = 0
        self.token: Optional[Token] = None

    def next_token(self) -> Token:
        self.state = lex_whitespace
        while self.token is None:
            self.state = self.state(self)
        return self.token

    def emit(self, t: TokenType) -> None:
        self.token = Token(t, self.input[self.start:self.pos])
        self.start = self.pos

    def next(self) -> Optional[str]:
        if len(self.input) <= self.pos:
            self.width = 0
            return None
        r = self.input[self.pos]
        self.pos += 1
        return r

    def backup(self) -> None:
        self.pos -= 1

    def ignore(self) -> None:
        self.start = self.pos

    def peek(self) -> Optional[str]:
        r: Optional[str] = self.next()
        self.backup()
        return r

    def accept(self, valid: str) -> bool:
        if valid.find(self.next()) >= 0:
            return True
        self.backup()
        return False

    def accept_run(self, valid: str) -> None:
        while valid.find(self.next()) >= 0:
            pass
        self.backup()

    def errorf(self, s: str) -> None:
        self.token = Token(TokenType.TokenError, s)


StateFn = Callable[[Lexer], 'StateFn']


def lex_whitespace(l: Lexer) -> Optional[StateFn]:
    r: Optional[str] = l.next()
    while r == ' ' or r == '\t' or r == '\n' or r == '\r':
        r = l.next()
    l.backup()
    l.ignore()
    r = l.next()
    if r is None:
        return lex_EOF
    elif r == ';':
        return lex_comment
    elif r == '(':
        return lex_open_paren
    elif r == ')':
        return lex_close_paren
    elif r == '"':
        return lex_string
    elif r == '\'':
        return lex_quote
    elif r == '`':
        return lex_quasiquote
    elif r == ',':
        return lex_unquote
    elif r == '+' or r == '-' or r.isdigit():
        l.backup()
        return lex_number
    elif is_alpha_numeric(r):
        return lex_identifier
    else:
        return l.errorf(f'unexpected character: {r}')


def lex_EOF(l: Lexer) -> Optional[StateFn]:
    l.emit(TokenType.TokenEOF)
    return None

def lex_quote(l: Lexer) -> StateFn:
    l.emit(TokenType.TokenQuote)
    return lex_whitespace

def lex_quasiquote(l: Lexer) -> StateFn:
    l.emit(TokenType.TokenQuasiquote)
    return lex_whitespace

def lex_unquote(l: Lexer) -> StateFn:
    if not l.accept('@'):
        l.emit(TokenType.TokenUnquote)
    else:
        l.emit(TokenType.TokenUnquoteSplicing)
    return lex_whitespace

def lex_unquote_splicing(l: Lexer) -> StateFn:
    l.emit(TokenType.TokenUnquoteSplicing)
    return lex_whitespace

def lex_string(l: Lexer) -> Optional[StateFn]:
    r = l.next()
    while r != '"':
        if r == '\\':
            r = l.next()
        if r is None:
            return l.errorf('read: expected a closing \'\\\'')
        r = l.next()
    l.emit(TokenType.TokenStringLiteral)
    return lex_whitespace

def lex_open_paren(l: Lexer) -> StateFn:
    l.emit(TokenType.TokenOpenParen)
    return lex_whitespace

def lex_close_paren(l: Lexer) -> StateFn:
    l.emit(TokenType.TokenCloseParen)
    return lex_whitespace

def lex_comment(l: Lexer) -> StateFn:
    r = l.next()
    while r != '\n':
        r = l.next()
    return lex_whitespace

def lex_identifier(l: Lexer) -> StateFn:
    r = l.next()
    while is_alpha_numeric(r):
        r = l.next()
    l.backup()
    l.emit(TokenType.TokenIdentifier)
    return lex_whitespace

def lex_number(l: Lexer) -> Optional[StateFn]:
    is_float: bool = False
    has_flag: bool = l.accept('+-')
    digits: str = '0123456789'
    if l.accept('0') and l.accept('xX'):
        digits = '0123456789abcdefABCDEF'
    l.accept_run(digits)
    if l.accept('.'):
        is_float = True
        l.accept_run(digits)
    if l.accept('eE'):
        l.accept('+-')
        l.accept_run('0123456789')
    r = l.peek()
    if is_alpha_numeric(r):
        l.next()
        return l.errorf(f'bad number syntax: {l.input[l.start:l.pos]}')
    if has_flag and l.start+1 == l.pos:
        return lex_identifier
    if is_float:
        l.emit(TokenType.TokenFloatLiteral)
    else:
        l.emit(TokenType.TokenIntegerLiteral)
    return lex_whitespace

def is_alpha_numeric(r: str) -> bool:
    if '!#$%&|*+-/:<=>?@^_~'.find(r) >= 0:
        return True
    return r == '.' or r.isalpha() or r.isdigit()
