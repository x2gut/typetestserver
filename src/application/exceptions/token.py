from src.application.exceptions.base import ApplicationException


class TokenException(ApplicationException):
    pass


class ExpiredSignature(TokenException):
    pass


class InvalidTokenPayload(TokenException):
    pass


class InvalidTokenType(TokenException):
    pass


class VerificationError(TokenException):
    pass
