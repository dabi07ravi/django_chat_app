from rest_framework.exceptions import APIException

class AppException(APIException):
    status_code = 400

    def __init__(self, message="Something went wrong", code="ERROR", status_code=400):
        self.status_code = status_code
        self.detail = {
            "success": False,
            "message": message,
            "code": code
        }


class UserAlreadyExists(AppException):
    def __init__(self):
        super().__init__("User already exists", "USER_EXISTS", 400)


class UserNotFound(AppException):
    def __init__(self):
        super().__init__("User not found", "USER_NOT_FOUND", 404)


class UnauthorizedAction(AppException):
    def __init__(self):
        super().__init__("Not allowed", "UNAUTHORIZED", 403)

class InvalidCredentials(AppException):
    def __init__(self):
        super().__init__("Invalid phone or password", "INVALID_CREDENTIALS", 401)


class InvalidPassword(AppException):
    def __init__(self):
        super().__init__("Invalid password", "INVALID_PASSWORD", 401)


class TokenInvalid(AppException):
    def __init__(self):
        super().__init__("Invalid or expired token", "TOKEN_INVALID", 401)

class ChatNotFound(AppException):
    def __init__(self):
        super().__init__("Chat not found", "CHAT_NOT_FOUND", 404)


class NotGroupChat(AppException):
    def __init__(self):
        super().__init__("This is not a group chat", "NOT_GROUP_CHAT", 400)


class NotGroupAdmin(AppException):
    def __init__(self):
        super().__init__("Only admin can perform this action", "NOT_GROUP_ADMIN", 403)


class CannotRemoveAdmin(AppException):
    def __init__(self):
        super().__init__("Cannot remove admin", "CANNOT_REMOVE_ADMIN", 400)


class UserNotInChat(AppException):
    def __init__(self):
        super().__init__("User is not part of this chat", "USER_NOT_IN_CHAT", 400)