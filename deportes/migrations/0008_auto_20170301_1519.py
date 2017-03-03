# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deportes', '0007_auto_20170301_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deporte',
            name='ficha_medica',
            field=models.ForeignKey(blank=True, to='deportes.FichaMedica', null=True),
            preserve_default=True,
        ),
    ]
