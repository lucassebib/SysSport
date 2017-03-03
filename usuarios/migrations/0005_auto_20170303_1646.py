# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_usuarioinvitado_contactos_de_urgencia'),
    ]

    operations = [
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
        migrations.AddField(
            model_name='alumno',
            name='datos_medicos',
            field=models.ForeignKey(blank=True, to='usuarios.DatosMedicos', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usuarioinvitado',
            name='datos_medicos',
            field=models.ForeignKey(blank=True, to='usuarios.DatosMedicos', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='persona',
            name='dni',
            field=models.BigIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
