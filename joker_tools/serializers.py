from rest_framework import serializers

from models import *


class EnvironmentVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentVariable
        fields = '__all__'
