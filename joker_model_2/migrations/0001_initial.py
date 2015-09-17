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
                ('regular_prop', models.FloatField(null=True)),
                ('reason_code_1', models.CharField(max_length=255, null=True)),
                ('reason_code_2', models.CharField(max_length=255, null=True)),
                ('reason_code_3', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='customer',
            unique_together=set([('id', 'source')]),
        ),
    ]
