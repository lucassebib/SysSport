# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import deportes.models
import usuarios.validators


class Migration(migrations.Migration):

    dependencies = [
        ('deportes', '0002_deporte_apto_para'),
    ]

    operations = [
        migrations.AddField(
            model_name='deporte',
            name='ficha_medica',
            field=models.FileField(blank=True, upload_to=deportes.models.generar_rutaID, validators=[usuarios.validators.valid_extension]),
            preserve_default=True,
        ),
    ]
