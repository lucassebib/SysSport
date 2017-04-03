# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import usuarios.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('deportes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('foto_perfil', models.ImageField(default=b'usuarios/fotos_de_perfil/None/default_profile.jpg', upload_to=b'usuarios/fotos_de_perfil/')),
                ('legajo', models.IntegerField(null=True, blank=True)),
                ('dni', models.BigIntegerField(null=True, blank=True)),
                ('ficha_medica', models.FileField(blank=True, upload_to=b'usuarios/fichas_medicas/', validators=[usuarios.validators.valid_extension])),
                ('is_active', models.BooleanField(default=False)),
                ('activation_key', models.CharField(max_length=40, blank=True)),
                ('key_expires', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Alumnos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactoDeUrgencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, null=True, blank=True)),
                ('apellido', models.CharField(max_length=100, null=True, blank=True)),
                ('parentezco', models.CharField(max_length=100, null=True, blank=True)),
                ('telefono', models.CharField(max_length=15, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DatosMedicos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grupo_sanguineo', models.IntegerField(default=3, choices=[(1, b'0-'), (2, b'0+'), (3, b'A-'), (4, b'A+'), (5, b'B-'), (6, b'B+'), (7, b'AB-'), (8, b'AB+')])),
                ('alergias', models.TextField(default=b'sin alergias')),
                ('toma_medicamentos', models.IntegerField(default=3, choices=[(1, b'NO'), (2, b'SI'), (3, b'NS/NC')])),
                ('medicamentos_cuales', models.TextField(default=b'sin medicacion')),
                ('tuvo_operaciones', models.IntegerField(default=3, choices=[(1, b'NO'), (2, b'SI'), (3, b'NS/NC')])),
                ('operaciones_cuales', models.TextField(default=b'sin operaciones')),
                ('tiene_osocial', models.IntegerField(default=3, choices=[(1, b'NO'), (2, b'SI'), (3, b'NS/NC')])),
                ('osocial_cual', models.TextField(default=b'sin obra social')),
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
                ('nro_departamento', models.CharField(max_length=2, null=True, blank=True)),
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
                ('dni', models.BigIntegerField(null=True, blank=True)),
                ('fecha_nacimiento', models.DateField(null=True, blank=True)),
                ('telefono', models.CharField(max_length=15, null=True, blank=True)),
                ('foto_perfil', models.ImageField(default=b'usuarios/fotos_de_perfil/None/default_profile.jpg', upload_to=b'usuarios/fotos_de_perfil/')),
                ('sexo', models.IntegerField(default=1, choices=[(1, b'Masculino'), (2, b'Femenino')])),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
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
                ('ficha_medica', models.FileField(upload_to=b'usuarios/fichas_medicas/', blank=True)),
                ('contactos_de_urgencia', models.ManyToManyField(to='usuarios.ContactoDeUrgencia', null=True, verbose_name=b'Contacto de Urgencia', blank=True)),
                ('datos_medicos', models.ForeignKey(blank=True, to='usuarios.DatosMedicos', null=True)),
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
        migrations.AddField(
            model_name='alumno',
            name='datos_medicos',
            field=models.ForeignKey(blank=True, to='usuarios.DatosMedicos', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alumno',
            name='lista_deporte',
            field=models.ManyToManyField(to='deportes.Deporte', verbose_name=b'Deportes Inscripto'),
            preserve_default=True,
        ),
    ]
