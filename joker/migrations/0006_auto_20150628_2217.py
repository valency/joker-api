# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('joker', '0005_auto_20150618_1748'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('export_mode', models.CharField(default=b'csv', max_length=16, choices=[(b'csv', b'Comma-Separated Values'), (b'xlsx', b'Microsoft Excel Workbook')])),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='conf',
            field=models.OneToOneField(to='joker.Configuration'),
        ),
    ]
