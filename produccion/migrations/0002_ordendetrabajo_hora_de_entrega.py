# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordendetrabajo',
            name='hora_de_entrega',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
