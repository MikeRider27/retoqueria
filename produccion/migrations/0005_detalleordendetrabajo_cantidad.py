# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0004_ordendetrabajo_gestion_de_compra'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleordendetrabajo',
            name='cantidad',
            field=models.DecimalField(default=1.0, max_digits=4, decimal_places=2),
        ),
    ]
