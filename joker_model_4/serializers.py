from rest_framework import serializers

from models import *


class CustomerSerializer(serializers.ModelSerializer):
    betline_standard_part = serializers.ListField(source='betline_standard_part_array')
    betline_exotic_part = serializers.ListField(source='betline_exotic_part_array')

    class Meta:
        model = Customer
        fields = '__all__'
