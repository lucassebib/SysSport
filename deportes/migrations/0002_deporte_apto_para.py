# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deportes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deporte',
            name='apto_para',
            field=models.IntegerField(default=3, choices=[(1, b'Solo Masculino'), (2, b'Solo Femenino'), (3, b'Mixto')]),
            preserve_default=True,
        ),
    ]
