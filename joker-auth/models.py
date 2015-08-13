from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User)
    ticket = models.CharField(max_length=36, null=True)

    def __str__(self):
        return self.id
