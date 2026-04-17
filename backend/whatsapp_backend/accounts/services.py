from .repository import UserRepository
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.exceptions import AuthenticationFailed

class UserService:

    @staticmethod
    def register_user(data):
        existing = UserRepository.find_by_phone(data["phone"])
        if existing:
            raise Exception("User already exists")

        data["password"] = make_password(data["password"])
        return UserRepository.create_user(data)

    @staticmethod
    def login_user(phone, password):
        user = UserRepository.find_by_phone(phone)

        if not user:
            raise AuthenticationFailed("User not found")

        if not check_password(password, user["password"]):
            raise AuthenticationFailed("Invalid password")

        return user