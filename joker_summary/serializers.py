from rest_framework import serializers

from joker_summary.models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting


class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
