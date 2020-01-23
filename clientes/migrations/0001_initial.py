# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('razon_social', models.CharField(max_length=100, verbose_name=b'Nombre o raz\xc3\xb3n social')),
                ('ruc', models.CharField(max_length=20, null=True, verbose_name=b'RUC', blank=True)),
                ('direccion', models.CharField(max_length=200, null=True, verbose_name=b'direcci\xc3\xb3n', blank=True)),
                ('telefono', models.CharField(max_length=50, null=True, verbose_name=b'tel\xc3\xa9fono', blank=True)),
                ('email', models.CharField(max_length=100, null=True, verbose_name=b'e-mail', blank=True)),
                ('observaciones', models.TextField(max_length=500, null=True, blank=True)),
            ],
        ),
    ]
