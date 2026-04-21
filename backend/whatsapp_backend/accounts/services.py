from .repository import UserRepository
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.exceptions import AuthenticationFailed
from core.file_service import save_file
from core.exceptions import (
    UserNotFound,
    UserAlreadyExists,
    InvalidPassword,
)


class UserService:

    @staticmethod
    def register_user(data):
        existing = UserRepository.find_by_phone(data["phone"])
        if existing:
            raise UserAlreadyExists()

        data["password"] = make_password(data["password"])
        return UserRepository.create_user(data)

    @staticmethod
    def login_user(phone, password):
        user = UserRepository.find_by_phone(phone)

        if not user:
            raise UserNotFound()

        if not check_password(password, user["password"]):
            raise InvalidPassword()

        return user

    @staticmethod
    def upload_profile_pic(user_id, file):

        url = save_file(file)

        UserRepository.update_profile_pic(user_id, url)

        return {"profile_pic": url}
