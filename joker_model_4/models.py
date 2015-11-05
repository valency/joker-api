from django.db import models

CUST_INV_PART_COUNT = 83
CUST_INV_EXOTIC_COUNT = 83


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
    ar = models.FloatField(null=True)
    inv_standard = models.FloatField(null=True)
    div_standard = models.FloatField(null=True)
    rr_standard = models.FloatField(null=True)
    ar_exotic = models.FloatField(null=True)
    inv_exotic = models.FloatField(null=True)
    div_exotic = models.FloatField(null=True)
    rr_exotic = models.FloatField(null=True)
    betline_standard = models.IntegerField(null=True)
    betline_exotic = models.IntegerField(null=True)
    mtg_num = models.IntegerField(null=True)
    mtg_num_exotic = models.IntegerField(null=True)
    end_bal = models.FloatField(null=True)
    recharge_times = models.IntegerField(null=True)
    recharge_amount = models.FloatField(null=True)
    withdraw_times = models.IntegerField(null=True)
    withdraw_amount = models.FloatField(null=True)
    betline_1_half = models.IntegerField(null=True)
    betline_2_half = models.IntegerField(null=True)
    betline_recent = models.IntegerField(null=True)
    betline_exotic_recent = models.IntegerField(null=True)
    exotic_half_increase = models.IntegerField(null=True)
    exotic_half_increase_ratio = models.FloatField(null=True)
    exotic_percent_1_half = models.FloatField(null=True)
    exotic_percent_2_half = models.FloatField(null=True)
    exotic_percent_half_increase = models.FloatField(null=True)
    exotic_betline_percent = models.FloatField(null=True)
    score_hp_preference = models.FloatField(null=True)
    score_hp_participation = models.FloatField(null=True)
    hp_preference_reason_code_1 = models.CharField(max_length=255, null=True)
    hp_preference_reason_code_2 = models.CharField(max_length=255, null=True)
    hp_preference_reason_code_3 = models.CharField(max_length=255, null=True)
    hp_preference_reason_code_4 = models.CharField(max_length=255, null=True)
    hp_participation_reason_code_1 = models.CharField(max_length=255, null=True)
    hp_participation_reason_code_2 = models.CharField(max_length=255, null=True)
    hp_participation_reason_code_3 = models.CharField(max_length=255, null=True)
    hp_participation_reason_code_4 = models.CharField(max_length=255, null=True)
    betline_standard_part = models.CharField(max_length=8196, null=True)
    betline_exotic_part = models.CharField(max_length=8196, null=True)

    @property
    def betline_standard_part_array(self):
        return self.betline_standard_part.split(";")

    @property
    def betline_exotic_part_array(self):
        return self.betline_exotic_part.split(";")

    def __str__(self):
        return self.source + ":" + str(self.id)

    class Meta:
        unique_together = ('id', 'source')
