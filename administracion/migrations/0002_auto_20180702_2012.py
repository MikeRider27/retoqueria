# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0002_auto_20180702_2012'),
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flujocaja',
            name='forma_pago',
            field=models.ForeignKey(verbose_name=b'Forma de Pago', to='ventas.FormaPago', null=True),
        ),
        migrations.AddField(
            model_name='flujocaja',
            name='sesion',
            field=models.ForeignKey(to='ventas.Sesion', null=True),
        ),
        migrations.AddField(
            model_name='flujocaja',
            name='venta',
            field=models.ForeignKey(to='ventas.Venta', null=True),
        ),
        migrations.CreateModel(
            name='IngresoDinero',
            fields=[
            ],
            options={
                'verbose_name': 'Ingreso de Dinero',
                'proxy': True,
                'verbose_name_plural': 'Ingresos de Dinero',
            },
            bases=('administracion.flujocaja',),
        ),
        migrations.CreateModel(
            name='RetiroDinero',
            fields=[
            ],
            options={
                'verbose_name': 'Retiro de Dinero',
                'proxy': True,
                'verbose_name_plural': 'Retiros de Dinero',
            },
            bases=('administracion.flujocaja',),
        ),
    ]
