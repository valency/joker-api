# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('avatar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleMeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='intersection',
            name='p',
            field=models.ForeignKey(to='avatar.Point', null=True),
        ),
        migrations.AlterField(
            model_name='pathfragment',
            name='p',
            field=models.TextField(max_length=65535, null=True),
        ),
        migrations.AlterField(
            model_name='road',
            name='length',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='road',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='road',
            name='speed',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='road',
            name='type',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='angle',
            field=models.IntegerField(null=True),
        ),
        migrations.RemoveField(
            model_name='sample',
            name='meta',
        ),
        migrations.AlterField(
            model_name='sample',
            name='occupy',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='speed',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='src',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='trajectory',
            name='path',
            field=models.ForeignKey(to='avatar.Path', null=True),
        ),
        migrations.AlterField(
            model_name='trajectory',
            name='trace',
            field=models.ForeignKey(to='avatar.Trace', null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='meta',
            field=models.ManyToManyField(to='avatar.SampleMeta'),
        ),
    ]
