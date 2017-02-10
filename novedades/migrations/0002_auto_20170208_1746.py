# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
        ('novedades', '0001_initial'),
        ('deportes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='novedades',
            name='autor',
            field=models.ForeignKey(to='usuarios.Profesor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='novedades',
            name='categoria',
            field=models.ManyToManyField(to='deportes.Deporte'),
            preserve_default=True,
        ),
    ]
