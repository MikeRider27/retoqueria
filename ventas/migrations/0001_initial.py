# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0001_initial'),
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('precio', models.DecimalField(max_digits=15, decimal_places=2)),
                ('orden_de_trabajo', models.ForeignKey(to='produccion.OrdenDeTrabajo')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('factura', models.CharField(max_length=50)),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('condicion', models.CharField(default=b'CO', max_length=2, verbose_name=b'Condicion de Venta', choices=[(b'CO', b'CONTADO'), (b'CR', b'CREDITO')])),
                ('anulado', models.BooleanField(default=False)),
                ('total', models.DecimalField(default=0, max_digits=15, decimal_places=2)),
                ('condicion_pago', models.CharField(default=b'CAN', max_length=3, null=True, verbose_name=b'Condicion de Pago', choices=[(b'PAR', b'PARCIAL'), (b'CAN', b'CANCELACION')])),
                ('cliente', models.ForeignKey(to='clientes.Cliente')),
            ],
        ),
        migrations.AddField(
            model_name='detalleventa',
            name='venta',
            field=models.ForeignKey(to='ventas.Venta'),
        ),
    ]
