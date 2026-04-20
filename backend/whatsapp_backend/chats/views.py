from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    CreateChatSerializer,
    CreateGroupSerializer,
    AddMemberSerializer,
    RemoveMemberSerializer,
)
from .services import ChatService
from core.utils import get_user_from_token


class CreateChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateChatSerializer(data=request.data)

        if serializer.is_valid():
            user = get_user_from_token(request)
            sender_id = user._id
            receiver_id = serializer.validated_data["receiver_id"]
            chat = ChatService.create_or_get_chat(sender_id, receiver_id)

            return Response(chat, status=201)

        return Response(serializer.errors, status=400)


class UserChatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_user_from_token(request)
        sender_id = user._id
        chats = ChatService.get_user_chats(sender_id)

        return Response(chats)


class CreateGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateGroupSerializer(data=request.data)

        if serializer.is_valid():
            admin_id = get_user_from_token(request)

            group = ChatService.create_group(
                admin_id._id,
                serializer.validated_data["users"],
                serializer.validated_data["name"],
            )

            return Response(group, status=201)

        return Response(serializer.errors, status=400)


class AddMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddMemberSerializer(data=request.data)

        if serializer.is_valid():
            admin_id = get_user_from_token(request)

            result = ChatService.add_member(
                serializer.validated_data["chat_id"],
                admin_id._id,
                serializer.validated_data["user_id"],
            )

            return Response(result, status=200)

        return Response(serializer.errors, status=400)


class RemoveMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RemoveMemberSerializer(data=request.data)

        if serializer.is_valid():
            admin_id = get_user_from_token(request)

            result = ChatService.remove_member(
                serializer.validated_data["chat_id"],
                 admin_id._id,
                serializer.validated_data["user_id"],
            )

            return Response(result, status=200)

        return Response(serializer.errors, status=400)
