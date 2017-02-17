import enum

EOF = -1

class TokenType(enum.Enum):
    TokenError = 0
    TokenEOF = 1

    TokenIdentifier = 2

    TokenStringLiteral = 3
    TokenIntegerLiteral = 4
    TokenFloatLiteral = 5
    TokenBooleanLiteral = 6

    TokenQuote = 7
    TokenQuasiquote = 8
    TokenUnquote = 9
    TokenUnquoteSplicing = 10

    TokenOpenParen = 11
    TokenCloseParen = 12
    TokenOpenSquare = 13
    TokenCloseSquare = 14

class Token(object):

    def __init__(self, ty: TokenType, val: str) -> None:
        self.ty: TokenType = ty
        self.val: str = val

