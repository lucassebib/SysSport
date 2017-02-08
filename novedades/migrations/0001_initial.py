# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Novedades',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100)),
                ('contenido', tinymce.models.HTMLField()),
                ('fecha_publicacion', models.DateTimeField(auto_now_add=True)),
                ('imagen', models.ImageField(null=True, upload_to=b'fotos_posts', blank=True)),
                ('visibilidad', models.IntegerField(default=3, choices=[(1, b'Todos'), (2, b'Todos los Usuarios Registrados'), (3, b'Solo los Usuarios del Deporte')])),
            ],
            options={
                'verbose_name_plural': 'Novedades',
            },
            bases=(models.Model,),
        ),
    ]