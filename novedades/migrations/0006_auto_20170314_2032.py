# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('novedades', '0005_auto_20170314_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacion',
            name='notificar_a',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
