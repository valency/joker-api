# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('joker', '0004_customer_cust_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='cust_code',
            field=models.CharField(max_length=4, null=True),
        ),
    ]
