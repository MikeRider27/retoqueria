# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='tipo',
            field=models.IntegerField(default=0, editable=False, choices=[(0, b'Modista'), (1, b'Costura')]),
        ),
    ]
