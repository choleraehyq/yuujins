class UndefinedIdentifier(Exception):
    def __init__(self, message: str) -> None:
        super(UndefinedIdentifier, self).__init__(message)
