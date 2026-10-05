from django.urls import path, include
from rest_framework.routers import DefaultRouter
from habits_app.views import HabitViewSet, PublicHabitListAPIView

router = DefaultRouter()
# Регистрируем ViewSet для CRUD-операций
router.register(r'habits', HabitViewSet, basename='habits')

urlpatterns = [
    # Список публичных привычек выносим на отдельный эндпоинт
    path('habits/public/', PublicHabitListAPIView.as_view(), name='public_habits'),
    # Подключаем роутер для CRUD
    path('', include(router.urls)),
]
