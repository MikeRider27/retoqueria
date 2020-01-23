# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0007_detalleordendetrabajo_liquidado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordendetrabajo',
            name='modista',
            field=models.ForeignKey(default=4, to='funcionarios.Funcionario', null=True),
        ),
    ]
