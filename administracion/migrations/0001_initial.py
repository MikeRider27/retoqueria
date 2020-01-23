# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaFlujoCaja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=20)),
                ('tipo', models.CharField(max_length=2, choices=[(b'IN', b'Ingreso'), (b'EG', b'Egreso')])),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='FlujoCaja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=5, choices=[(b'IN', b'Ingreso'), (b'EG', b'Egreso')])),
                ('motivo', models.CharField(max_length=200, null=True, blank=True)),
                ('monto', models.DecimalField(max_digits=14, decimal_places=2)),
                ('fecha', models.DateTimeField(default=datetime.datetime.now)),
                ('disponible', models.DecimalField(default=0, max_digits=14, decimal_places=2)),
                ('categoria', models.ForeignKey(to='administracion.CategoriaFlujoCaja', null=True)),
            ],
        ),
    ]
