# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0005_detalleordendetrabajo_cantidad'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='detalleordendetrabajo',
            options={'verbose_name': 'Servicio', 'verbose_name_plural': 'Servicios'},
        ),
    ]
