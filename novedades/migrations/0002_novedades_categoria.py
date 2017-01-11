# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novedades', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='novedades',
            name='categoria',
            field=models.ManyToManyField(to='novedades.Deporte'),
            preserve_default=True,
        ),
    ]
