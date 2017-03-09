# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='carrera',
            field=models.IntegerField(default=1, choices=[(1, b'ISI'), (2, b'IQ'), (3, b'IEM'), (4, b'LAR'), (5, b'TSP'), (6, b'OTRO')]),
            preserve_default=True,
        ),
    ]
