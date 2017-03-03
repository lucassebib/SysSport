# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import usuarios.validators


class Migration(migrations.Migration):

    dependencies = [
        ('deportes', '0004_auto_20170301_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichamedica',
            name='ficha_medica',
            field=models.FileField(blank=True, upload_to=b'usuarios/deportes/fichas_medicas/', validators=[usuarios.validators.valid_extension]),
            preserve_default=True,
        ),
    ]
