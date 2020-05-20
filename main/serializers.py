from rest_framework import serializers
from .models import NextMinTrajectory
class NextMinTrajectorySerializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=NextMinTrajectory



