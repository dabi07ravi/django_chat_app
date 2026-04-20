from django.urls import path
from .views import (
    CreateChatView,
    UserChatsView,
    CreateGroupView,
    AddMemberView,
    RemoveMemberView,
)

urlpatterns = [
    path("", UserChatsView.as_view()),
    path("create/", CreateChatView.as_view()),
    path("group/create/", CreateGroupView.as_view()),
    path("group/add_member/", AddMemberView.as_view()),
    path("group/remove_member/", RemoveMemberView.as_view()),
]
