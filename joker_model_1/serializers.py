from rest_framework import serializers

from models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer


class CustomerSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSet