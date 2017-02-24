# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_auto_20170224_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuarioinvitado',
            name='contactos_de_urgencia',
        ),
    ]
