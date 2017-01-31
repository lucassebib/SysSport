# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
        ('canchas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancha',
            name='direccion',
            field=models.ForeignKey(blank=True, to='usuarios.Direccion', null=True),
            preserve_default=True,
        ),
    ]
