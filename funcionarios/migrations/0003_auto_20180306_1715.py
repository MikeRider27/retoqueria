# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0006_auto_20180306_1715'),
        ('funcionarios', '0002_funcionario_activo'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleDeLiquidacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subtotal', models.DecimalField(default=0, max_digits=15, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Liquidacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('total', models.DecimalField(default=0, max_digits=15, decimal_places=2)),
                ('modista', models.ForeignKey(to='funcionarios.Funcionario')),
            ],
        ),
        migrations.AddField(
            model_name='detalledeliquidacion',
            name='liquidacion',
            field=models.ForeignKey(to='funcionarios.Liquidacion'),
        ),
        migrations.AddField(
            model_name='detalledeliquidacion',
            name='servicio',
            field=models.ForeignKey(to='produccion.DetalleOrdenDeTrabajo'),
        ),
    ]
