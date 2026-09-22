class ShortenerError(Exception):
    pass


class LinkNotFoundError(ShortenerError):
    def __init__(self, code: str) -> None:
        super().__init__(f"No link is registered for code '{code}'")
        self.code = code


class DuplicatedCodeError(ShortenerError):
    def __init__(self, code: str) -> None:
        super().__init__(f"Code '{code}' is already taken")
        self.code = code


class CodeGenerationFailedError(ShortenerError):
    pass
