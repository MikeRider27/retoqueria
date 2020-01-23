# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0002_ordendetrabajo_hora_de_entrega'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordendetrabajo',
            name='dias_para_prueba',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ordendetrabajo',
            name='dias_post_prueba',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
