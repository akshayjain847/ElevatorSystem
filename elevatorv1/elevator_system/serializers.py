from rest_framework import serializers
from .models import Elevator, Request

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'

class ElevatorSerializer(serializers.ModelSerializer):
    requests = RequestSerializer(many=True, read_only=True)

    class Meta:
        model = Elevator
        fields = '__all__'
