# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('joker', '0003_auto_20150610_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='cust_code',
            field=models.IntegerField(null=True),
        ),
    ]
