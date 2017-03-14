# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novedades', '0004_novedades_autor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novedades',
            name='categoria',
            field=models.ManyToManyField(to='deportes.Deporte', null=True, blank=True),
            preserve_default=True,
        ),
    ]
