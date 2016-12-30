# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novedades', '0002_auto_20161229_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='lista_deporte',
            field=models.ManyToManyField(to=b'novedades.Deporte', verbose_name=b'Deportes Inscripto'),
        ),
        migrations.AlterField(
            model_name='persona',
            name='foto_perfil',
            field=models.ImageField(null=True, upload_to=b'fotos_de_perfil/', blank=True),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='lista_deporte',
            field=models.ManyToManyField(to=b'novedades.Deporte', verbose_name=b'Deportes Inscriptos'),
        ),
    ]
