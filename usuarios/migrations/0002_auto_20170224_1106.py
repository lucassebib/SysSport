# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import usuarios.validators


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='ficha_medica',
            field=models.FileField(blank=True, upload_to=b'usuarios/fichas_medicas/', validators=[usuarios.validators.valid_extension]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='persona',
            name='foto_perfil',
            field=models.ImageField(default=b'usuarios/fotos_de_perfil/None/default_profile.jpg', upload_to=b'usuarios/fotos_de_perfil/'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuarioinvitado',
            name='ficha_medica',
            field=models.FileField(upload_to=b'usuarios/fichas_medicas/', blank=True),
            preserve_default=True,
        ),
    ]
