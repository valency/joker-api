from rest_framework import serializers

from models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Account
        fields = ('id', 'user', 'last_log_in', 'last_change_of_password')
