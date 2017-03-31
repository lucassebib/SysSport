# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_auto_20170329_1700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumno',
            name='activation_key',
        ),
        migrations.RemoveField(
            model_name='alumno',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='alumno',
            name='key_expires',
        ),
    ]
