# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
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
                ('fecha_publicacion', models.DateTimeField(auto_now_add=True)),
                ('imagen', models.ImageField(null=True, upload_to=b'fotos_posts', blank=True)),
                ('visibilidad', models.IntegerField(default=3, choices=[(1, b'Todos'), (2, b'Todos los Usuarios Registrados'), (3, b'Solo los Usuarios del Deporte')])),
            ],
            options={
                'verbose_name_plural': 'Novedades',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('dni', models.IntegerField()),
                ('fecha_nacimiento', models.DateField()),
                ('telefono', models.IntegerField()),
                ('foto_perfil', models.ImageField(null=True, upload_to=b'fotos_de_perfil/', blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('persona_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='novedades.Persona')),
                ('legajo', models.IntegerField()),
                ('ficha_medica', models.FileField(upload_to=b'fichas_medicas/', blank=True)),
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
                ('legajo', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Profesores',
            },
            bases=('novedades.persona',),
        ),
        migrations.CreateModel(
            name='UsuarioInvitado',
            fields=[
                ('persona_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='novedades.Persona')),
                ('institucion', models.CharField(max_length=100)),
                ('ficha_medica', models.FileField(upload_to=b'fichas_medicas/', blank=True)),
            ],
            options={
                'verbose_name_plural': 'UsuariosInvitados',
            },
            bases=('novedades.persona',),
        ),
        migrations.AddField(
            model_name='persona',
            name='lista_deporte',
            field=models.ManyToManyField(to='novedades.Deporte', verbose_name=b'Deportes Inscripto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='novedades',
            name='autor',
            field=models.ForeignKey(to='novedades.Profesor'),
            preserve_default=True,
        ),
    ]
