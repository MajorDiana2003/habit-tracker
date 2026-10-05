from rest_framework import serializers
from users.models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    # Пароль делаем доступным только для записи, чтобы он не возвращался в ответе API
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'telegram_chat_id')

    def create(self, validated_data):
        # Используем метод create_user, чтобы пароль правильно захешировался
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            telegram_chat_id=validated_data.get('telegram_chat_id', '')
        )
        return user
