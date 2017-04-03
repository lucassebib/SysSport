# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Peticionesservidor',
            fields=[
                ('peticion', models.IntegerField(null=True, db_column=b'PETICION', blank=True)),
                ('idpetici_n', models.AutoField(serialize=False, primary_key=True, db_column='IDPETICI\xd3N')),
                ('idexterna', models.CharField(max_length=20, db_column=b'IDEXTERNA', blank=True)),
                ('estado', models.SmallIntegerField(null=True, db_column=b'ESTADO', blank=True)),
                ('statussalida', models.TextField(db_column=b'STATUSSALIDA', blank=True)),
                ('fecha', models.DateTimeField(null=True, db_column=b'FECHA', blank=True)),
                ('parametro1', models.TextField(db_column=b'PARAMETRO1', blank=True)),
                ('parametro2', models.TextField(db_column=b'PARAMETRO2', blank=True)),
                ('parametro3', models.TextField(db_column=b'PARAMETRO3', blank=True)),
                ('instancia', models.CharField(max_length=20, db_column=b'INSTANCIA', blank=True)),
            ],
            options={
                'db_table': 'PeticionesServidor',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
