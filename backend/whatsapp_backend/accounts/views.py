from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, ProfilePicSerializer
from .services import UserService
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from core.utils import get_user_from_token



class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            UserService.register_user(serializer.validated_data)
            return Response({"message": "User created"}, status=201)

        return Response(serializer.errors, status=400)


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = UserService.login_user(
                serializer.validated_data["phone"],
                serializer.validated_data["password"],
            )

            refresh = RefreshToken()
            refresh["mongo_id"] = str(user["_id"])

            return Response(
                {"access": str(refresh.access_token), "refresh": str(refresh)}
            )

        return Response(serializer.errors, status=400)


class UploadProfilePicView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProfilePicSerializer(data=request.data)

        if serializer.is_valid():
            user_id = get_user_from_token(request)

            result = UserService.upload_profile_pic(
                user_id._id, serializer.validated_data["profile_pic"]
            )

            return Response(result)

        return Response(serializer.errors, status=400)
