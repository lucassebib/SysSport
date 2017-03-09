# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('canchas', '0002_cancha_direccion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cancha',
            name='deportes_aptos',
        ),
    ]
