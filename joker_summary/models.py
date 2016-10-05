from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models


class Customer(models.Model):
    cust_id = models.IntegerField(db_column='cust_id', blank=True, primary_key=True)
    segment_code = models.TextField(db_column='segment_code', blank=True, null=True)
    age = models.IntegerField(db_column='age', blank=True, null=True)
    registration_date = models.DateTimeField(db_column='registration_date', blank=True, null=True)
    is_new_cust_ytd = JSONField(db_column='is_new_cust_ytd', blank=True, null=True)
    is_new_cust_pytd = JSONField(db_column='is_new_cust_pytd', blank=True, null=True)
    major_channel = models.TextField(db_column='major_channel', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cust_demo'


class Meeting(models.Model):
    global_mtg_seqno = models.IntegerField(db_column='global_mtg_seqno', blank=True, primary_key=True)
    season_mtg_seqno = models.IntegerField(db_column='season_mtg_seqno', blank=True, null=True)
    mtg_date = models.DateTimeField(db_column='mtg_date', blank=True, null=True)
    season = models.IntegerField(db_column='season', blank=True, null=True)
    mtg_status = models.TextField(db_column='mtg_status', blank=True, null=True)
    mtg_loc = models.TextField(db_column='mtg_loc', blank=True, null=True)
    mtg_type = models.TextField(db_column='mtg_type', blank=True, null=True)
    num_race = models.IntegerField(db_column='num_race', blank=True, null=True)
    days_since_last_mtg = models.TextField(db_column='days_since_last_mtg', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mtg_info'


class Summary(models.Model):
    trans_id = models.IntegerField(db_column='trans_id', blank=True, primary_key=True)
    cust_id = models.ForeignKey(Customer, db_column='cust_id')
    global_mtg_seqno = models.ForeignKey(Meeting, db_column="global_mtg_seqno")
    standard_turnover = models.FloatField(db_column='standard_turnover', blank=True, null=True)
    exotic_turnover = models.FloatField(db_column='exotic_turnover', blank=True, null=True)
    standard_betline = models.IntegerField(db_column='standard_betline', blank=True, null=True)
    exotic_betline = models.IntegerField(db_column='exotic_betline', blank=True, null=True)
    standard_turnover_ytd = models.FloatField(db_column='standard_turnover_ytd', blank=True, null=True)
    exotic_turnover_ytd = models.FloatField(db_column='exotic_turnover_ytd', blank=True, null=True)
    standard_betline_ytd = models.IntegerField(db_column='standard_betline_ytd', blank=True, null=True)
    exotic_betline_ytd = models.IntegerField(db_column='exotic_betline_ytd', blank=True, null=True)
    active_rate_ytd = models.FloatField(db_column='active_rate_ytd', blank=True, null=True)
    active_mtg_ytd = models.FloatField(db_column='active_mtg_ytd', blank=True, null=True)
    race_num = models.IntegerField(db_column='race_num', blank=True, null=True)
    turnover_bettype_details = JSONField(db_column='turnover_bettype_details', blank=True, null=True)
    turnover_channel_details = JSONField(db_column='turnover_channel_details', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'summary'
