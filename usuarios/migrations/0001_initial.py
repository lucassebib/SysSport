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
            name='ContactoDeUrgencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, null=True, blank=True)),
                ('apellido', models.CharField(max_length=100, null=True, blank=True)),
                ('parentezco', models.CharField(max_length=100, null=True, blank=True)),
                ('telefono', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('calle', models.CharField(max_length=100, null=True, blank=True)),
                ('altura', models.IntegerField(null=True, blank=True)),
                ('piso', models.IntegerField(null=True, blank=True)),
                ('nro_departamento', models.IntegerField(null=True, blank=True)),
                ('provincia', models.CharField(max_length=100, null=True, blank=True)),
                ('localidad', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Direcciones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('dni', models.IntegerField(null=True, blank=True)),
                ('fecha_nacimiento', models.DateField(null=True, blank=True)),
                ('telefono', models.IntegerField(null=True, blank=True)),
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
                ('legajo', models.IntegerField(null=True, blank=True)),
                ('ficha_medica', models.FileField(upload_to=b'fichas_medicas/', blank=True)),
                ('carrera', models.IntegerField(default=1, choices=[(1, b'ISI'), (2, b'IQ'), (3, b'IEM'), (4, b'LAR'), (5, b'TSP')])),
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
                ('legajo', models.IntegerField(null=True, blank=True)),
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
                'verbose_name_plural': 'Usuarios Invitados',
            },
            bases=('usuarios.persona',),
        ),
        migrations.AddField(
            model_name='persona',
            name='direccion',
            field=models.ForeignKey(blank=True, to='usuarios.Direccion', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='persona',
            name='lista_deporte',
            field=models.ManyToManyField(to='deportes.Deporte', verbose_name=b'Deportes Inscripto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contactodeurgencia',
            name='direccion',
            field=models.ForeignKey(blank=True, to='usuarios.Direccion', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alumno',
            name='contactos_de_urgencia',
            field=models.ManyToManyField(to='usuarios.ContactoDeUrgencia', null=True, verbose_name=b'Contacto de Urgencia', blank=True),
            preserve_default=True,
        ),
    ]
