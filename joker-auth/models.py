from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class Account(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return self.id

    def auth(self, password):
        user = authenticate(username=self.user.username, password=password)
        return user is not None and user.is_active
