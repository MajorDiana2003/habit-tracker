from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import UserRegisterView

urlpatterns = [
    # Регистрация
    path('register/', UserRegisterView.as_view(), name='register'),

    # Авторизация (получение токена) и его обновление
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
