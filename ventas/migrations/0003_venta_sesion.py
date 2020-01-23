# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0002_auto_20180702_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='sesion',
            field=models.ForeignKey(blank=True, to='ventas.Sesion', null=True),
        ),
    ]
