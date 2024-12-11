from src.domain.common.exceptions.base import AppException


class UserAlreadyExists(AppException):
    pass


class UserNotFound(AppException):
    pass
