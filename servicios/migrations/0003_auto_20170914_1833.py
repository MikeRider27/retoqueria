# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0002_servicio_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='tipo',
            field=models.CharField(default=b'modista', max_length=10, choices=[(b'modista', b'Modista'), (b'costura', b'Costurera')]),
        ),
    ]
