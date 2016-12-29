# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deporte',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Deportes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Novedades',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100)),
                ('contenido', tinymce.models.HTMLField()),
                ('fecha_publicacion', models.DateField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Novedades',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('legajo', models.IntegerField()),
                ('dni', models.IntegerField()),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('fecha_nacimiento', models.DateField()),
                ('telefono', models.IntegerField()),
                ('email', models.EmailField(max_length=75)),
                ('foto_perfil', models.ImageField(upload_to=b'fotos_de_perfil/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('persona_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='novedades.Persona')),
                ('ficha_medica', models.FileField(upload_to=b'fichas_medicas/', blank=True)),
                ('lista_deporte', models.ManyToManyField(to='novedades.Deporte')),
            ],
            options={
                'verbose_name_plural': 'Alumnos',
            },
            bases=('novedades.persona',),
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('persona_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='novedades.Persona')),
                ('lista_deporte', models.ManyToManyField(to='novedades.Deporte')),
            ],
            options={
                'verbose_name_plural': 'Profesores',
            },
            bases=('novedades.persona',),
        ),
        migrations.AddField(
            model_name='novedades',
            name='autor',
            field=models.ForeignKey(to='novedades.Profesor'),
            preserve_default=True,
        ),
    ]
