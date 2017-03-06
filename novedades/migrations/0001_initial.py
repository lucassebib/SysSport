# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texto', models.TextField(verbose_name=b'comentario')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_autor_comentario', models.IntegerField()),
                ('autor_comentario', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Novedades',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100)),
                ('contenido', tinymce.models.HTMLField()),
                ('fecha_publicacion', models.DateTimeField(auto_now_add=True)),
                ('imagen', models.ImageField(null=True, upload_to=b'fotos_posts', blank=True)),
                ('visibilidad', models.IntegerField(default=2, choices=[(1, b'Todas las personas'), (2, b'Todos los Usuarios Registrados'), (3, b'Solo los Usuarios del Deporte')])),
            ],
            options={
                'verbose_name_plural': 'Novedades',
            },
            bases=(models.Model,),
        ),
    ]
