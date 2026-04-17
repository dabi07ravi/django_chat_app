from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from bson import ObjectId

from core.db import db
from core.user import MongoUser



class MongoJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]
            decoded = AccessToken(token)

            mongo_id = decoded.get("mongo_id")

            if not mongo_id:
                raise AuthenticationFailed("Invalid token")

            user = db["users"].find_one({"_id": ObjectId(mongo_id)})

            if not user:
                raise AuthenticationFailed("User not found")

            user["_id"] = str(user["_id"])

            return (MongoUser(user), None)

        except Exception:
            raise AuthenticationFailed("Invalid token")