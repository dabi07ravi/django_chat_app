from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import SendMessageSerializer
from .services import MessageService
from core.utils import get_user_from_token


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)

        if serializer.is_valid():
            user = get_user_from_token(request)
            sender_id = user._id

            message = MessageService.send_message(
                serializer.validated_data["chat_id"],
                sender_id,
                serializer.validated_data["content"],
            )

            return Response(message, status=201)

        return Response(serializer.errors, status=400)


class ChatMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id):
        page = max(1, int(request.GET.get("page", 1)))
        limit = min(20, int(request.GET.get("limit", 20)))
        user = get_user_from_token(request)
        sender_id = user._id
        result = MessageService.get_messages(chat_id, sender_id, page, limit)
        return Response({"success": True, **result})
