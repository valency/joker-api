from rest_framework import serializers

from models import *


class CustomerSerializer(serializers.ModelSerializer):
    inv_part = serializers.ListField(source='inv_part_array')

    class Meta:
        model = Customer
        fields = '__all__'
