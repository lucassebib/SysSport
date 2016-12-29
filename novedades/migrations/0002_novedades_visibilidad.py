# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novedades', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='novedades',
            name='visibilidad',
            field=models.IntegerField(default=3, choices=[(1, b'Todos'), (2, b'UsuariosRegistrados'), (3, b'UsuarioDeporte')]),
            preserve_default=True,
        ),
    ]
