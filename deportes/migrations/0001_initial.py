# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import usuarios.validators


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
                ('apto_para', models.IntegerField(default=3, choices=[(1, b'Solo Masculino'), (2, b'Solo Femenino'), (3, b'Mixto')])),
            ],
            options={
                'verbose_name_plural': 'Deportes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FichaMedica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ficha_medica', models.FileField(blank=True, upload_to=b'usuarios/deportes/fichas_medicas/', validators=[usuarios.validators.valid_extension])),
                ('descripcion', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='deporte',
            name='ficha_medica',
            field=models.ForeignKey(blank=True, to='deportes.FichaMedica', null=True),
            preserve_default=True,
        ),
    ]
