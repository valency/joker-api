from rest_framework import serializers

from models import *


class Customer1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Customer1


class Customer2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Customer2


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer
    conf = ConfigurationSerializer

    class Meta:
        model = Account


class EnvironmentVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnviromentVariable
