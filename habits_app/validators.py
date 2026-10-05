from rest_framework.serializers import ValidationError


class RewardAndAssociatedHabitValidator:
    """
    Исключает одновременный выбор связанной привычки и указания вознаграждения.
    """
    def __call__(self, attrs):
        reward = attrs.get('reward')
        associated_habit = attrs.get('associated_habit')

        if reward and associated_habit:
            raise ValidationError(
                "Нельзя одновременно заполнить поле вознаграждения и поле связанной привычки. "
                "Можно заполнить только одно из двух полей."
            )


class TimeToCompleteValidator:
    """
    Проверяет, что время выполнения должно быть не больше 120 секунд.
    """
    def __call__(self, attrs):
        time_to_complete = attrs.get('time_to_complete')

        if time_to_complete and time_to_complete > 120:
            raise ValidationError(
                "Время выполнения должно быть не больше 120 секунд."
            )


class AssociatedHabitIsPleasantValidator:
    """
    В связанные привычки могут попадать только привычки с признаком приятной привычки.
    """
    def __call__(self, attrs):
        associated_habit = attrs.get('associated_habit')

        if associated_habit and not associated_habit.is_pleasant:
            raise ValidationError(
                "В связанные привычки могут попадать только привычки с признаком приятной привычки."
            )


class PleasantHabitNoRewardOrAssociationValidator:
    """
    У приятной привычки не может быть вознаграждения или связанной привычки.
    """
    def __call__(self, attrs):
        is_pleasant = attrs.get('is_pleasant')
        reward = attrs.get('reward')
        associated_habit = attrs.get('associated_habit')

        if is_pleasant:
            if reward or associated_habit:
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                )


class PeriodicityValidator:
    """
    Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
    """
    def __call__(self, attrs):
        periodicity = attrs.get('periodicity')

        if periodicity and periodicity > 7:
            raise ValidationError(
                "Нельзя выполнять привычку реже, чем 1 раз в 7 дней (максимум 7 дней)."
            )
