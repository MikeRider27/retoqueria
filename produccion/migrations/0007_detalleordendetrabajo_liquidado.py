# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0006_auto_20180306_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleordendetrabajo',
            name='liquidado',
            field=models.BooleanField(default=False),
        ),
    ]
