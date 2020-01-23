# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0001_initial'),
        ('materiales', '0001_initial'),
        ('funcionarios', '0001_initial'),
        ('depositos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleretiro',
            name='detalle_orden_de_trabajo',
            field=models.ForeignKey(verbose_name=b'trabajo', blank=True, to='produccion.DetalleOrdenDeTrabajo', null=True),
        ),
        migrations.AddField(
            model_name='detalleretiro',
            name='material',
            field=models.ForeignKey(to='materiales.Material'),
        ),
        migrations.AddField(
            model_name='detalleretiro',
            name='retiro',
            field=models.ForeignKey(to='depositos.Retiro'),
        ),
        migrations.AddField(
            model_name='detalledevolucion',
            name='deposito',
            field=models.ForeignKey(to='depositos.Deposito'),
        ),
        migrations.AddField(
            model_name='detalledevolucion',
            name='detalle_retiro',
            field=models.ForeignKey(verbose_name=b'Material', to='depositos.DetalleRetiro', null=True),
        ),
        migrations.AddField(
            model_name='detalledevolucion',
            name='devolucion',
            field=models.ForeignKey(to='depositos.Devolucion'),
        ),
        migrations.AddField(
            model_name='detallebaja',
            name='baja',
            field=models.ForeignKey(to='depositos.Baja'),
        ),
        migrations.AddField(
            model_name='detallebaja',
            name='material',
            field=models.ForeignKey(to='materiales.Material'),
        ),
        migrations.AddField(
            model_name='detallealta',
            name='alta',
            field=models.ForeignKey(to='depositos.Alta'),
        ),
        migrations.AddField(
            model_name='detallealta',
            name='material',
            field=models.ForeignKey(to='materiales.Material'),
        ),
        migrations.AddField(
            model_name='baja',
            name='deposito',
            field=models.ForeignKey(to='depositos.Deposito'),
        ),
        migrations.AddField(
            model_name='baja',
            name='funcionario',
            field=models.ForeignKey(to='funcionarios.Funcionario'),
        ),
        migrations.AddField(
            model_name='alta',
            name='deposito',
            field=models.ForeignKey(to='depositos.Deposito'),
        ),
        migrations.AddField(
            model_name='alta',
            name='funcionario',
            field=models.ForeignKey(to='funcionarios.Funcionario'),
        ),
    ]
