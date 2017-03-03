# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import deportes.models
import usuarios.validators


class Migration(migrations.Migration):

    dependencies = [
        ('deportes', '0003_deporte_ficha_medica'),
    ]

    operations = [
        migrations.CreateModel(
            name='FichaMedica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ficha_medica', models.FileField(blank=True, upload_to=deportes.models.generar_rutaID, validators=[usuarios.validators.valid_extension])),
                ('descripcion', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='deporte',
            name='ficha_medica',
            field=models.ForeignKey(to='deportes.FichaMedica', blank=True),
            preserve_default=True,
        ),
    ]
