from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from .services import UserService
from rest_framework_simplejwt.tokens import RefreshToken

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
                serializer.validated_data["password"]
            )

            refresh = RefreshToken()
            refresh["user_id"] = str(user["_id"])

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })

        return Response(serializer.errors, status=400)