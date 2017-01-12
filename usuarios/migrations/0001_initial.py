# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('deportes', '0001_initial'),
    ]

    operations = [
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
                ('persona_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='usuarios.Persona')),
                ('legajo', models.IntegerField()),
                ('ficha_medica', models.FileField(upload_to=b'fichas_medicas/', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Alumnos',
            },
            bases=('usuarios.persona',),
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('persona_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='usuarios.Persona')),
                ('legajo', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Profesores',
            },
            bases=('usuarios.persona',),
        ),
        migrations.CreateModel(
            name='UsuarioInvitado',
            fields=[
                ('persona_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='usuarios.Persona')),
                ('institucion', models.CharField(max_length=100)),
                ('ficha_medica', models.FileField(upload_to=b'fichas_medicas/', blank=True)),
            ],
            options={
                'verbose_name_plural': 'UsuariosInvitados',
            },
            bases=('usuarios.persona',),
        ),
        migrations.AddField(
            model_name='persona',
            name='lista_deporte',
            field=models.ManyToManyField(to='deportes.Deporte', verbose_name=b'Deportes Inscripto'),
            preserve_default=True,
        ),
    ]
