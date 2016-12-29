# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novedades', '0003_novedades_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novedades',
            name='visibilidad',
            field=models.IntegerField(default=3, choices=[(1, b'Todos'), (2, b'Todos los Usuarios Registrados'), (3, b'Solo los Usuarios del Deporte')]),
        ),
    ]
