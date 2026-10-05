from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from users.models import User
from users.serializers import UserRegisterSerializer

class UserRegisterView(CreateAPIView):
    """
    Эндпоинт для регистрации нового пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    # Регистрация должна быть доступна всем без авторизации
    permission_classes = [AllowAny]

