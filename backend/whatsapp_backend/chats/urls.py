from django.urls import path
from .views import CreateChatView, UserChatsView

urlpatterns = [
    path('', UserChatsView.as_view()),
    path('create/', CreateChatView.as_view()),
]