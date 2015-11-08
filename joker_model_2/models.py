from django.db import models

CUST_INV_PART_COUNT = 83


class Customer(models.Model):
    dbpk = models.AutoField(primary_key=True)
    id = models.IntegerField()
    source = models.CharField(max_length=255)
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
    chance_to_be_regular = models.FloatField(null=True)
    reason_code_1 = models.CharField(max_length=255, null=True)
    reason_code_2 = models.CharField(max_length=255, null=True)
    reason_code_3 = models.CharField(max_length=255, null=True)
    reason_code_4 = models.CharField(max_length=255, null=True)
    active_rate_previous_83 = models.FloatField(null=True)
    inv_part = models.CharField(max_length=8196, null=True)

    @property
    def inv_part_array(self):
        if self.inv_part:
            return self.inv_part.split(";")
        else:
            return None

    def __str__(self):
        return self.source + ":" + str(self.id)

    class Meta:
        unique_together = ('id', 'source')
