from rest_framework import serializers
from habits_app.models import Habit
from habits_app.validators import (
    RewardAndAssociatedHabitValidator,
    TimeToCompleteValidator,
    AssociatedHabitIsPleasantValidator,
    PleasantHabitNoRewardOrAssociationValidator,
    PeriodicityValidator
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit

        fields = (
            'id',
            'user',
            'place',
            'time',
            'action',
            'is_pleasant',
            'related_habit',
            'periodicity_days',
            'reward',
            'duration_seconds',
            'is_public',
        )

        read_only_fields = ('id', 'user')

        validators = [
            RewardAndAssociatedHabitValidator(),
            TimeToCompleteValidator(),
            AssociatedHabitIsPleasantValidator(),
            PleasantHabitNoRewardOrAssociationValidator(),
            PeriodicityValidator(),
        ]
