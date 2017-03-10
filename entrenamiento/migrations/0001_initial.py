# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entrenamiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dia', models.IntegerField(default=1, choices=[(1, b'Lunes'), (2, b'Martes'), (3, b'Miercoles'), (4, b'Jueves'), (5, b'Viernes'), (6, b'Sabado'), (7, b'Domingo')])),
                ('horario_inicio', models.IntegerField(default=1, verbose_name=b'Hora de Inicio', choices=[(1, b'07:00'), (2, b'07:30'), (3, b'08:00'), (4, b'08:30'), (5, b'09:00'), (6, b'09:30'), (7, b'10:00'), (8, b'10:30'), (9, b'11:00'), (10, b'11:30'), (11, b'12:00'), (12, b'12:30'), (13, b'13:00'), (14, b'13:30'), (15, b'14:00'), (16, b'14:30'), (17, b'15:00'), (18, b'15:30'), (20, b'16:00'), (21, b'16:30'), (22, b'17:00'), (23, b'17:30'), (24, b'18:00'), (25, b'18:30'), (26, b'19:00'), (27, b'19:30'), (28, b'20:00'), (29, b'20:30'), (30, b'21:00'), (31, b'21:30'), (32, b'22:00'), (33, b'22:30'), (34, b'23:00'), (35, b'23:30'), (36, b'00:00'), (37, b'00:30')])),
                ('horario_fin', models.IntegerField(default=2, verbose_name=b'Hora de Finalizacion', choices=[(1, b'07:00'), (2, b'07:30'), (3, b'08:00'), (4, b'08:30'), (5, b'09:00'), (6, b'09:30'), (7, b'10:00'), (8, b'10:30'), (9, b'11:00'), (10, b'11:30'), (11, b'12:00'), (12, b'12:30'), (13, b'13:00'), (14, b'13:30'), (15, b'14:00'), (16, b'14:30'), (17, b'15:00'), (18, b'15:30'), (20, b'16:00'), (21, b'16:30'), (22, b'17:00'), (23, b'17:30'), (24, b'18:00'), (25, b'18:30'), (26, b'19:00'), (27, b'19:30'), (28, b'20:00'), (29, b'20:30'), (30, b'21:00'), (31, b'21:30'), (32, b'22:00'), (33, b'22:30'), (34, b'23:00'), (35, b'23:30'), (36, b'00:00'), (37, b'00:30')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
