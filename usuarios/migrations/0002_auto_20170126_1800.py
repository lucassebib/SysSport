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
            field=models.FileField(blank=True, upload_to=b'fichas_medicas/', validators=[usuarios.validators.valid_extension]),
            preserve_default=True,
        ),
    ]
