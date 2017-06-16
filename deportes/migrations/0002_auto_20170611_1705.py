# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deportes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deporte',
            name='ficha_medica',
            field=models.ForeignKey(related_name='ficha_deporte', blank=True, to='deportes.FichaMedica', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichamedica',
            name='descripcion',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
