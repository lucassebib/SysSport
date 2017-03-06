# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
        ('novedades', '0001_initial'),
        ('deportes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='novedades',
            name='autor',
            field=models.ForeignKey(blank=True, to='usuarios.Profesor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='novedades',
            name='categoria',
            field=models.ManyToManyField(to='deportes.Deporte'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='novedades',
            name='lista_comentarios',
            field=models.ManyToManyField(to='novedades.Comentario', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notificacion',
            name='notificar_a',
            field=models.ForeignKey(to='usuarios.Profesor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notificacion',
            name='novedad',
            field=models.ForeignKey(to='novedades.Novedades'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comentario',
            name='autor',
            field=models.ForeignKey(to='usuarios.Persona'),
            preserve_default=True,
        ),
    ]
