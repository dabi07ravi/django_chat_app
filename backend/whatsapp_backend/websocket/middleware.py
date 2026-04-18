from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from bson import ObjectId
from core.db import db


class JWTAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):

        query_string = scope["query_string"].decode()
        query_params = parse_qs(query_string)

        token = query_params.get("token")

        if token:
            try:
                token = token[0]
                decoded = AccessToken(token)

                mongo_id = decoded.get("mongo_id")

                user = db["users"].find_one({"_id": ObjectId(mongo_id)})

                if user:
                    user["_id"] = str(user["_id"])
                    scope["user_id"] = user["_id"]
                else:
                    scope["user_id"] = None

            except Exception:
                scope["user_id"] = None
        else:
            scope["user_id"] = None

        return await super().__call__(scope, receive, send)