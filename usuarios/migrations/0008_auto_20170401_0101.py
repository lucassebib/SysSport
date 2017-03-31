# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_auto_20170330_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='key_expires',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
