from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from user.apps import UserConfig
from user.views import *

app_name = UserConfig.name

urlpatterns = [
    path('list/', UserListAPIView.as_view(), name='users'),
    path('register/', UserCreate.as_view(), name='user_register'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user_delete'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
