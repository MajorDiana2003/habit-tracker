from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.serializers import ValidationError
from habits_app.models import Habit
from habits_app.validators import (
    RewardAndAssociatedHabitValidator,
    PeriodicityValidator
)


User = get_user_model()


class HabitTestCase(APITestCase):

    def setUp(self):
        """Подготовка данных перед каждым тестом."""
        self.user = User.objects.create_user(
            email="test_user@example.com",
            password="testpassword123"
        )
        self.other_user = User.objects.create_user(
            email="other_user@example.com",
            password="otherpassword123"
        )

        self.client.force_authenticate(user=self.user)

        # Создаем базовую приятную привычку
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Принять контрастный душ",
            is_pleasant=True,
            is_public=True
        )

    def test_create_habit_success(self):
        """Успешное создание привычки с валидными данными."""
        url = reverse('habits-list')
        data = {
            "place": "Офис",
            "time": "12:00:00",
            "action": "Сделать разминку",
            "is_pleasant": False,
            "periodicity_days": 2,
            "reward": "Выпить вкусный кофе",
            "is_public": True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_habit_pagination_and_list(self):
        """Проверка работы пагинации (ограничение вывода по 5 элементов)."""
        url = reverse('habits-list')
        for i in range(5):
            Habit.objects.create(
                user=self.user,
                place="Где-то",
                time="10:00:00",
                action=f"Тестовое действие {i}",
                is_pleasant=True
            )

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)

    def test_validator_reward_and_associated_habit(self):
        """Валидатор: Запрещено одновременно указывать награду и связанную привычку."""
        validator = RewardAndAssociatedHabitValidator()
        bad_attrs = {
            "related_habit": self.pleasant_habit,
            "reward": "Съесть шоколадку"
        }

        # Проверяем, что класс валидатора выбрасывает ValidationError при некорректных данных
        with self.assertRaises(ValidationError):
            validator(bad_attrs)

    def test_validator_periodicity(self):
        """Валидатор: Запрещено выставлять периодичность реже 1 раза в 7 дней."""
        validator = PeriodicityValidator()
        bad_attrs = {
            "periodicity_days": 10
        }

        with self.assertRaises(ValidationError):
            validator(bad_attrs)

    def test_permission_owner_crud(self):
        """Права доступа: Чужой пользователь получает 404 при попытке доступа к чужой привычке."""
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="19:00:00",
            action="Медитация"
        )

        self.client.force_authenticate(user=self.other_user)

        url = reverse('habits-detail', args=[habit.id])
        data = {"action": "Взлом привычки"}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
