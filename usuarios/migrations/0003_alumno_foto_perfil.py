# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_alumno_dni'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='foto_perfil',
            field=models.ImageField(default=b'usuarios/fotos_de_perfil/None/default_profile.jpg', upload_to=b'usuarios/fotos_de_perfil/'),
            preserve_default=True,
        ),
    ]
