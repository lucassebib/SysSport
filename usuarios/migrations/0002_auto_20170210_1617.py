# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='sexo',
            field=models.IntegerField(default=1, choices=[(1, b'Masculino'), (2, b'Femenino')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usuarioinvitado',
            name='contactos_de_urgencia',
            field=models.ManyToManyField(to='usuarios.ContactoDeUrgencia', null=True, verbose_name=b'Contacto de Urgencia', blank=True),
            preserve_default=True,
        ),
    ]
