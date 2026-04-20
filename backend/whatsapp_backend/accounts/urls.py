from django.urls import path
from .views import RegisterView, LoginView, UploadProfilePicView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('upload-profile-pic/', UploadProfilePicView.as_view()),
]