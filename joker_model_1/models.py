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
    end_bal = models.FloatField(null=True)
    recharge_times = models.IntegerField(null=True)
    recharge_amount = models.FloatField(null=True)
    withdraw_times = models.IntegerField(null=True)
    withdraw_amount = models.FloatField(null=True)
    active_rate_previous_83 = models.FloatField(null=True)
    to_per_mtg = models.FloatField(null=True)
    betline_per_mtg = models.FloatField(null=True)
    avg_bet_size = models.FloatField(null=True)
    to_ytd_growth = models.FloatField(null=True)
    to_recent_growth = models.FloatField(null=True)
    to_per_mtg_ytd_growth = models.FloatField(null=True)
    to_per_mtg_recent_growth = models.FloatField(null=True)
    betline_per_mtg_ytd_growth = models.FloatField(null=True)
    betline_per_mtg_recent_growth = models.FloatField(null=True)
    avg_bet_size_ytd_growth = models.FloatField(null=True)
    avg_bet_size_recent_growth = models.FloatField(null=True)
    active_rate_ytd_growth = models.FloatField(null=True)
    active_rate_recent_growth = models.FloatField(null=True)
    turnover_ratio = models.FloatField(null=True)
    active_rate_ratio = models.FloatField(null=True)
    recovery_rate_ratio = models.FloatField(null=True)
    amplification = models.FloatField(null=True)
    grow_prop = models.FloatField(null=True)
    decline_prop = models.FloatField(null=True)
    grow_reason_code_1 = models.CharField(max_length=255, null=True)
    grow_reason_code_2 = models.CharField(max_length=255, null=True)
    grow_reason_code_3 = models.CharField(max_length=255, null=True)
    grow_reason_code_4 = models.CharField(max_length=255, null=True)
    decline_reason_code_1 = models.CharField(max_length=255, null=True)
    decline_reason_code_2 = models.CharField(max_length=255, null=True)
    decline_reason_code_3 = models.CharField(max_length=255, null=True)
    decline_reason_code_4 = models.CharField(max_length=255, null=True)
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


class CustomerSet(models.Model):
    dbpk = models.AutoField(primary_key=True)
    id = models.CharField(max_length=36)
    name = models.CharField(max_length=255)
    create_time = models.DateTimeField()
    cust = models.ForeignKey(Customer)
    cluster = models.IntegerField(null=True)
    cluster_time = models.DateTimeField(null=True)
    cluster_features = models.CharField(max_length=8196, null=True)
    cluster_count = models.IntegerField(null=True)
    cluster_metric = models.CharField(max_length=32, null=True)

    @property
    def cluster_features_array(self):
        if self.cluster_features:
            return self.cluster_features.split(";")
        else:
            return None

    def __str__(self):
        return str(self.id) + ":" + str(self.cluster)

    class Meta:
        unique_together = ('id', 'cust')
