# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novedades', '0002_novedades_visibilidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='novedades',
            name='imagen',
            field=models.ImageField(null=True, upload_to=b'fotos_posts', blank=True),
            preserve_default=True,
        ),
    ]
