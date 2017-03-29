# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_alumno_foto_perfil'),
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
            field=models.DateTimeField(default=datetime.date(2017, 3, 29)),
            preserve_default=True,
        ),
    ]
