from rest_framework import serializers

from django.contrib.auth.models import User
from models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = Account
