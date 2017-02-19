class PreparseError(Exception):

    def __init__(self, message) -> None:
        super(PreparseError, self).__init__(message)


class ParseError(Exception):

    def __init__(self, message) -> None:
        super(ParseError, self).__init__(message)



class ExpandError(Exception):

    def __init__(self, message) -> None:
        super(ExpandError, self).__init__(message)