# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('dbpk', models.AutoField(serialize=False, primary_key=True)),
                ('id', models.IntegerField()),
                ('source', models.CharField(max_length=255)),
                ('segment', models.CharField(max_length=4, null=True)),
                ('age', models.IntegerField(null=True)),
                ('gender', models.CharField(max_length=1, null=True)),
                ('yrs_w_club', models.IntegerField(null=True)),
                ('is_member', models.NullBooleanField(default=None)),
                ('is_hrs_owner', models.NullBooleanField(default=None)),
                ('major_channel', models.CharField(max_length=8, null=True)),
                ('mtg_num', models.IntegerField(null=True)),
                ('inv', models.FloatField(null=True)),
                ('div', models.FloatField(null=True)),
                ('rr', models.FloatField(null=True)),
                ('end_bal', models.FloatField(null=True)),
                ('recharge_times', models.IntegerField(null=True)),
                ('recharge_amount', models.FloatField(null=True)),
                ('withdraw_times', models.IntegerField(null=True)),
                ('withdraw_amount', models.FloatField(null=True)),
                ('grow_prop', models.FloatField(null=True)),
                ('decline_prop', models.FloatField(null=True)),
                ('grow_reason_code_1', models.CharField(max_length=255, null=True)),
                ('grow_reason_code_2', models.CharField(max_length=255, null=True)),
                ('grow_reason_code_3', models.CharField(max_length=255, null=True)),
                ('decline_reason_code_1', models.CharField(max_length=255, null=True)),
                ('decline_reason_code_2', models.CharField(max_length=255, null=True)),
                ('decline_reason_code_3', models.CharField(max_length=255, null=True)),
                ('inv_part', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True), size=83)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerSet',
            fields=[
                ('dbpk', models.AutoField(serialize=False, primary_key=True)),
                ('id', models.CharField(max_length=36)),
                ('name', models.CharField(max_length=255)),
                ('create_time', models.DateTimeField()),
                ('cluster_time', models.DateTimeField(null=True)),
                ('cluster_features', django.contrib.postgres.fields.ArrayField(null=True, base_field=models.CharField(max_length=32), size=None)),
                ('cluster', models.IntegerField(null=True)),
                ('cluster_count', models.IntegerField(null=True)),
                ('cust', models.ForeignKey(to='joker_model_1.Customer')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='customer',
            unique_together=set([('id', 'source')]),
        ),
        migrations.AlterUniqueTogether(
            name='customerset',
            unique_together=set([('id', 'cust')]),
        ),
    ]
