#coding: utf-8
""" Database of exceptions """


class BaseException(Exception):
    message = ''


class InvalidCredentials(BaseException):
    pass


class InvalidUsername(BaseException):
    pass


class InvalidPassword(BaseException):
    pass


class InvalidEmail(BaseException):
    pass


class PasswordMismatch(BaseException):
    pass


class UserNotFound(BaseException):
    pass


class UserAlreadyExist(BaseException):
    pass

class EmptyUserName(BaseException):
    pass


class UserNotHasRole(BaseException):
    pass


class UserAlreadyInRole(BaseException):
    pass


class ValidationError(BaseException):
    pass


class SessionNotFound(BaseException):
    pass


class RoleAlreadyExist(BaseException):
    pass


class RoleAlreadyEmpty(BaseException):
    pass


class InvalidRoleName(BaseException):
    pass


class RoleNotFound(BaseException):
    pass


class UserRoleNotFound(BaseException):
    pass


class InviteNotFound(BaseException):
    pass
