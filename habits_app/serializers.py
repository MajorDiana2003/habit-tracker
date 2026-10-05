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

        fields = '__all__'
        read_only_fields = ('user',)


        validators = [
            RewardAndAssociatedHabitValidator(),
            TimeToCompleteValidator(),
            AssociatedHabitIsPleasantValidator(),
            PleasantHabitNoRewardOrAssociationValidator(),
            PeriodicityValidator()
        ]
