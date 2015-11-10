from joker_auth.models import *


class EnvironmentVariable(models.Model):
    key = models.CharField(max_length=32, primary_key=True)
    value = models.CharField(max_length=255, null=True)
    last_update = models.DateTimeField()

    def __str__(self):
        return self.id
