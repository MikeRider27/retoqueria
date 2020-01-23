# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proveedores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaDeMaterial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'categor\xeda de materiales',
                'verbose_name_plural': 'categor\xedas de materiales',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=150, verbose_name=b'descripci\xc3\xb3n')),
                ('stock_actual', models.DecimalField(default=0, editable=False, max_digits=15, decimal_places=2)),
                ('stock_minimo', models.DecimalField(default=0, max_digits=15, decimal_places=2)),
                ('categoria', models.ForeignKey(verbose_name=b'categor\xc3\xada', to='materiales.CategoriaDeMaterial')),
                ('proveedores', models.ManyToManyField(to='proveedores.Proveedor', blank=True)),
            ],
            options={
                'verbose_name_plural': 'materiales',
            },
        ),
        migrations.CreateModel(
            name='UnidadDeMedida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('simbolo', models.CharField(max_length=10, null=True, verbose_name=b'S\xc3\xadmbolo', blank=True)),
            ],
            options={
                'verbose_name': 'unidad de medida',
                'verbose_name_plural': 'unidades de medida',
            },
        ),
        migrations.AddField(
            model_name='material',
            name='unidad_de_medida',
            field=models.ForeignKey(to='materiales.UnidadDeMedida'),
        ),
    ]
