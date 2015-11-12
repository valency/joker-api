from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.ForeignKey(User)
    previous_password = models.CharField(max_length=255, null=True)
    last_change_of_password = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.id)
