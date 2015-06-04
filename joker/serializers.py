from rest_framework import serializers

from models import *


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction


class CustomerSerializer(serializers.ModelSerializer):
    prediction = PredictionSerializer(many=True)

    class Meta:
        model = Customer
