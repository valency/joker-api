from rest_framework import serializers

from joker_model.models import *


class ModelResultMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelResultMaster


class ModelTypeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTypeMaster


class ReasonCodeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReasonCodeMaster
