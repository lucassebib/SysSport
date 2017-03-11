# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deportes', '0003_deporte_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deporte',
            name='foto',
            field=models.ImageField(default=b'usuarios/deportes/fotos_deportes/none/deporte_default.png', upload_to=b'usuarios/deportes/fotos_deportes/'),
            preserve_default=True,
        ),
    ]
