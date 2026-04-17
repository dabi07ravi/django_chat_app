from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CreateChatSerializer
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