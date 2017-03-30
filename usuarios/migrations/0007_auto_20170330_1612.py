# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_auto_20170330_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='activation_key',
            field=models.CharField(max_length=40, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alumno',
            name='is_active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alumno',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2017, 3, 30)),
            preserve_default=True,
        ),
    ]
