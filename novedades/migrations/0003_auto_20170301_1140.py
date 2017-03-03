# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novedades', '0002_auto_20170212_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novedades',
            name='visibilidad',
            field=models.IntegerField(default=2, choices=[(1, b'Todas las personas'), (2, b'Todos los Usuarios Registrados'), (3, b'Solo los Usuarios del Deporte')]),
            preserve_default=True,
        ),
    ]
