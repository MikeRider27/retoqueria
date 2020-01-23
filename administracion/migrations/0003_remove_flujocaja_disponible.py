# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0002_auto_20180702_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flujocaja',
            name='disponible',
        ),
    ]
