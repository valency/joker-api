from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class Customer1(models.Model):
    id = models.IntegerField(primary_key=True)
    segment = models.CharField(max_length=4, null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=1, null=True)
    yrs_w_club = models.IntegerField(null=True)
    is_member = models.NullBooleanField(default=None)
    is_hrs_owner = models.NullBooleanField(default=None)
    major_channel = models.CharField(max_length=8, null=True)
    mtg_num = models.IntegerField(null=True)
    inv = models.FloatField(null=True)
    div = models.FloatField(null=True)
    rr = models.FloatField(null=True)
    end_bal = models.FloatField(null=True)
    recharge_times = models.IntegerField(null=True)
    recharge_amount = models.FloatField(null=True)
    withdraw_times = models.IntegerField(null=True)
    withdraw_amount = models.FloatField(null=True)
    grow_prop = models.FloatField()
    decline_prop = models.FloatField()
    reason_code_1 = models.CharField(max_length=255, null=True)
    reason_code_2 = models.CharField(max_length=255, null=True)
    reason_code_3 = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.id


class Customer2(models.Model):
    id = models.IntegerField(primary_key=True)
    segment = models.CharField(max_length=4, null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=1, null=True)
    yrs_w_club = models.IntegerField(null=True)
    is_member = models.NullBooleanField(default=None)
    is_hrs_owner = models.NullBooleanField(default=None)
    major_channel = models.CharField(max_length=8, null=True)
    mtg_num = models.IntegerField(null=True)
    inv = models.FloatField(null=True)
    div = models.FloatField(null=True)
    rr = models.FloatField(null=True)
    regular_prop = models.FloatField()
    reason_code_1 = models.CharField(max_length=255, null=True)
    reason_code_2 = models.CharField(max_length=255, null=True)
    reason_code_3 = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.id


class Configuration(models.Model):
    export_mode = models.CharField(
        max_length=16,
        choices=(
            ('csv', 'Comma-Separated Values'),
            ('xlsx', 'Microsoft Excel Workbook')
        ),
        default='csv')

    def __str__(self):
        return self.id


class Account(models.Model):
    user = models.ForeignKey(User)
    conf = models.ForeignKey(Configuration)

    def __str__(self):
        return self.id

    def auth(self, password):
        user = authenticate(username=self.user.username, password=password)
        return user is not None and user.is_active
