# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0003_auto_20171011_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordendetrabajo',
            name='gestion_de_compra',
            field=models.BooleanField(default=False),
        ),
    ]
