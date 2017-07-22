# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('entrenamiento', '0002_auto_20170722_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrenamiento',
            name='hora_fin',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(24)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrenamiento',
            name='hora_inicio',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(24)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrenamiento',
            name='minutos_fin',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(59)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrenamiento',
            name='minutos_inicio',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(59)]),
            preserve_default=True,
        ),
    ]
