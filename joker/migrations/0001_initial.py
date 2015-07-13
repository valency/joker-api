# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('age', models.IntegerField(null=True)),
                ('gender', models.CharField(max_length=1, null=True)),
                ('yrs_w_club', models.IntegerField(null=True)),
                ('is_member', models.NullBooleanField(default=None)),
                ('is_hrs_owner', models.NullBooleanField(default=None)),
                ('major_channel', models.CharField(max_length=8, null=True)),
                ('mtg_num', models.IntegerField(null=True)),
                ('inv', models.FloatField(null=True)),
                ('inv_seg_1', models.FloatField(null=True)),
                ('inv_seg_2', models.FloatField(null=True)),
                ('inv_seg_3', models.FloatField(null=True)),
                ('div', models.FloatField(null=True)),
                ('rr', models.FloatField(null=True)),
                ('end_bal', models.FloatField(null=True)),
                ('recharge_times', models.IntegerField(null=True)),
                ('recharge_amount', models.FloatField(null=True)),
                ('withdraw_times', models.IntegerField(null=True)),
                ('withdraw_amount', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('prob', models.FloatField()),
                ('reason_code_1', models.CharField(max_length=255, null=True)),
                ('reason_code_2', models.CharField(max_length=255, null=True)),
                ('reason_code_3', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='prediction',
            field=models.ManyToManyField(to='joker.Prediction'),
        ),
    ]
