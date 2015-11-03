from rest_framework import serializers

from models import *


class CustomerSerializer(serializers.ModelSerializer):
    inv_part = serializers.ListField(source='inv_part_array')
    inv_exotic_part = serializers.ListField(source='inv_exotic_part_array')

    class Meta:
        model = Customer
