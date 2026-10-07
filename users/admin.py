from django.contrib import admin
from users.models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    # Показываем только самые нужные поля в списке
    list_display = ('id', 'email', 'telegram_chat_id', 'is_staff')
    # Позволяем редактировать ID чата прямо из списка, не заходя внутрь профиля!
    list_editable = ('telegram_chat_id',)
