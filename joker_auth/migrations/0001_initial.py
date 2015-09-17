# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=128)),
                ('ticket', models.CharField(max_length=36, null=True)),
                ('last_login', models.DateTimeField(null=True)),
                ('last_update', models.DateTimeField(null=True)),
                ('register_time', models.DateTimeField(null=True)),
            ],
        ),
    ]
