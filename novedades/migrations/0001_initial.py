# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deportes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texto', models.TextField(verbose_name=b'comentario')),
                ('autor', models.IntegerField(null=True, blank=True)),
                ('nombre_autor', models.CharField(max_length=150, null=True, blank=True)),
                ('is_persona', models.BooleanField(default=True)),
                ('fecha_comentario', models.DateTimeField(auto_now_add=True)),
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
                ('fecha_comentario', models.DateTimeField(auto_now_add=True)),
                ('notificar_a', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
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
                ('autor', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('categoria', models.ManyToManyField(to='deportes.Deporte', null=True, blank=True)),
                ('lista_comentarios', models.ManyToManyField(to='novedades.Comentario', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Novedades',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='notificacion',
            name='novedad',
            field=models.ForeignKey(to='novedades.Novedades'),
            preserve_default=True,
        ),
    ]
