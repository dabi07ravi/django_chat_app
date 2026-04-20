from django.urls import path
from .views import SendMessageView, ChatMessagesView

urlpatterns = [
    path("send/", SendMessageView.as_view()),
    path("<str:chat_id>/", ChatMessagesView.as_view()),

]
