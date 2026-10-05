from django.db import models
from django.conf import settings


class Habit(models.Model):
    """Модель привычки, адаптированная под базу данных Django."""

    # Связь с пользователем. При удалении пользователя удалятся и его привычки.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Создатель привычки",
        related_name="habits"
    )

    action = models.CharField(max_length=255, verbose_name="Действие")
    place = models.CharField(max_length=255, verbose_name="Место выполнения")
    time = models.TimeField(verbose_name="Время выполнения")

    is_pleasant = models.BooleanField(default=False, verbose_name="Признак приятной привычки")

    # Связанная привычка (самобытная связь self). Может быть пустой (blank=True, null=True).
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Связанная приятная привычка",
        related_name="dependent_habits"
    )

    # Периодичность выполнения в днях (по умолчанию ежедневная — 1)
    periodicity_days = models.PositiveIntegerField(default=1, verbose_name="Периодичность (в днях)")

    # Вознаграждение за выполнение (может быть пустым)
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вознаграждение")

    # Время на выполнение в секундах (по умолчанию 120 секунд)
    duration_seconds = models.PositiveIntegerField(default=120, verbose_name="Время на выполнение (в секундах)")

    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")

    class Meta:
        verbose_name = "Привилегия / Привычка"
        verbose_name_plural = "Привычки"
        ordering = ['id']

    def __str__(self):
        return f"{self.action} в {self.time} ({self.place})"

