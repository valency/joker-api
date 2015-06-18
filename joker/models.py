from django.db import models


class Prediction(models.Model):
    label = models.CharField(max_length=255)
    prob = models.FloatField()
    reason_code_1 = models.CharField(max_length=255, null=True)
    reason_code_2 = models.CharField(max_length=255, null=True)
    reason_code_3 = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.cust.id


class Customer(models.Model):
    id = models.IntegerField(primary_key=True)
    cust_code = models.IntegerField(null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=1, null=True)
    yrs_w_club = models.IntegerField(null=True)
    is_member = models.NullBooleanField(default=None)
    is_hrs_owner = models.NullBooleanField(default=None)
    major_channel = models.CharField(max_length=8, null=True)
    mtg_num = models.IntegerField(null=True)
    inv = models.FloatField(null=True)
    inv_seg_1 = models.FloatField(null=True)
    inv_seg_2 = models.FloatField(null=True)
    inv_seg_3 = models.FloatField(null=True)
    div = models.FloatField(null=True)
    rr = models.FloatField(null=True)
    end_bal = models.FloatField(null=True)
    recharge_times = models.IntegerField(null=True)
    recharge_amount = models.FloatField(null=True)
    withdraw_times = models.IntegerField(null=True)
    withdraw_amount = models.FloatField(null=True)
    prediction = models.ManyToManyField(Prediction)

    def __str__(self):
        return self.id

    def assign_pred(self, label, prob, reason_code_1, reason_code_2, reason_code_3):
        try:
            Prediction.objects.all().filter(customer=self, label=label).delete()
            pred = Prediction(label=label, prob=prob, reason_code_1=reason_code_1, reason_code_2=reason_code_2, reason_code_3=reason_code_3)
            pred.save()
            self.prediction.add(pred)
            self.save()
        except TypeError as exp:
            return exp.message
        return None
