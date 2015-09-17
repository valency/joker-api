# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EnviromentVariable',
            fields=[
                ('key', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('value', models.CharField(max_length=255, null=True)),
                ('last_update', models.DateTimeField()),
            ],
        ),
    ]
