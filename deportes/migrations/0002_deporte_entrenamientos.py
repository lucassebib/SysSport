# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrenamiento', '0001_initial'),
        ('deportes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deporte',
            name='entrenamientos',
            field=models.ManyToManyField(to='entrenamiento.Entrenamiento', null=True, verbose_name=b'Entrenamientos', blank=True),
            preserve_default=True,
        ),
    ]
