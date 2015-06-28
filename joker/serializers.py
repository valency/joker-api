from rest_framework import serializers

from models import *


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction


class CustomerSerializer(serializers.ModelSerializer):
    prediction = PredictionSerializer(many=True)

    class Meta:
        model = Customer


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class AccountSerializer(serializers.ModelSerializer):
    auth = UserSerializer
    conf = ConfigurationSerializer

    class Meta:
        model = Account
