# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administracion', '0001_initial'),
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50)),
                ('estado', models.BooleanField(default=False, choices=[(True, b'Abierta'), (False, b'Cerrada')])),
                ('disponible', models.IntegerField(default=0)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='FormaPago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(unique=True, max_length=15)),
                ('nombre', models.CharField(unique=True, max_length=30)),
                ('nombre_comprobante', models.CharField(max_length=30)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='MovimientoCaja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(default=datetime.datetime.now)),
                ('apertura', models.BooleanField(verbose_name=b'tipo', choices=[(True, b'Apertura'), (False, b'Cierre')])),
                ('efectivo', models.IntegerField(default=0)),
                ('caja', models.ForeignKey(to='ventas.Caja')),
                ('vendedor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sesion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_apertura', models.DateTimeField(default=datetime.datetime.now)),
                ('fecha_cierre', models.DateTimeField(null=True)),
                ('saldo_apertura', models.DecimalField(default=0, max_digits=14, decimal_places=2)),
                ('saldo_cierre', models.DecimalField(default=0, max_digits=14, decimal_places=2)),
                ('caja', models.ForeignKey(to='ventas.Caja')),
                ('vendedor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MovimientoFlujoCaja',
            fields=[
            ],
            options={
                'verbose_name': 'Movimiento de Caja',
                'proxy': True,
                'verbose_name_plural': 'Movimientos de Cajas',
            },
            bases=('administracion.flujocaja',),
        ),
        migrations.CreateModel(
            name='AperturaCaja',
            fields=[
            ],
            options={
                'verbose_name': 'Apertura de Caja',
                'proxy': True,
                'verbose_name_plural': 'Aperturas de Caja',
            },
            bases=('ventas.sesion',),
        ),
        migrations.CreateModel(
            name='CierreCaja',
            fields=[
            ],
            options={
                'verbose_name': 'Cierre de Caja',
                'proxy': True,
                'verbose_name_plural': 'Cierres de Caja',
            },
            bases=('ventas.sesion',),
        ),
        migrations.AddField(
            model_name='venta',
            name='forma_pago',
            field=models.ForeignKey(blank=True, to='ventas.FormaPago', null=True),
        ),
    ]
