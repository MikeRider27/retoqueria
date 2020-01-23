# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('ruc', models.CharField(max_length=20, null=True, verbose_name=b'RUC/CI Nro.', blank=True)),
                ('direccion', models.CharField(max_length=200, null=True, blank=True)),
                ('email', models.EmailField(max_length=100, null=True, blank=True)),
                ('fecha_de_ingreso', models.DateField(null=True, blank=True)),
                ('observaciones', models.TextField(max_length=500, null=True, blank=True)),
                ('usuario', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
