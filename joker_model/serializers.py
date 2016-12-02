from rest_framework import serializers

from joker_model.models import *


class ModelResultMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelResultMaster
        fields = '__all__'


class ModelTypeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTypeMaster
        fields = '__all__'


class ReasonCodeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReasonCodeMaster
        fields = '__all__'
