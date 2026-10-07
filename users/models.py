from django.contrib.auth.models import AbstractUser
from django.db import models
from users.managers import UserManager


class User(AbstractUser):
    # Убираем поле username, так как авторизация будет по email
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта"
    )

    telegram_chat_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="ID чата в Telegram",
        help_text="Необходим для отправки уведомлений ботом"
    )

    # Настраиваем вход по email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
