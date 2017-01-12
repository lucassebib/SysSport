# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deportes', '0001_initial'),
        ('novedades', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='novedades',
            name='categoria',
            field=models.ManyToManyField(to='deportes.Deporte'),
            preserve_default=True,
        ),
    ]
