from rest_framework.serializers import ValidationError


class RewardAndAssociatedHabitValidator:
    """Нельзя одновременно указывать вознаграждение и связанную привычку."""
    def __call__(self, attrs):
        reward = attrs.get("reward")
        related_habit = attrs.get("related_habit")

        if reward and related_habit:
            raise ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку."
            )


class TimeToCompleteValidator:
    """Время выполнения должно быть не больше 120 секунд."""
    def __call__(self, attrs):
        duration_seconds = attrs.get("duration_seconds")

        if duration_seconds is not None and duration_seconds > 120:
            raise ValidationError(
                "Время выполнения должно быть не больше 120 секунд."
            )


class AssociatedHabitIsPleasantValidator:
    """Связанная привычка должна быть приятной."""
    def __call__(self, attrs):
        related_habit = attrs.get("related_habit")

        if related_habit and not related_habit.is_pleasant:
            raise ValidationError(
                "Связанная привычка должна быть приятной."
            )


class PleasantHabitNoRewardOrAssociationValidator:
    """У приятной привычки не может быть вознаграждения или связанной привычки."""
    def __call__(self, attrs):
        if attrs.get("is_pleasant") and (
            attrs.get("reward") or attrs.get("related_habit")
        ):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )


class PeriodicityValidator:
    """Периодичность должна быть от 1 до 7 дней."""
    def __call__(self, attrs):
        periodicity_days = attrs.get("periodicity_days")

        if periodicity_days is not None and not (1 <= periodicity_days <= 7):
            raise ValidationError(
                "Периодичность должна быть от 1 до 7 дней."
            )
