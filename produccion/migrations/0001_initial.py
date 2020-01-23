# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0003_auto_20170914_1833'),
        ('clientes', '0001_initial'),
        ('funcionarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleOrdenDeTrabajo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('precio', models.DecimalField(max_digits=15, decimal_places=2)),
                ('observaciones', models.TextField(null=True, blank=True)),
                ('categoria_servicio', models.ForeignKey(verbose_name=b'Categoria de servicio', to='servicios.CategoriaDeServicio', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrdenDeTrabajo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('revision', models.IntegerField(default=1, editable=False)),
                ('fecha_de_ingreso', models.DateField(default=datetime.date.today)),
                ('fecha_de_entrega', models.DateField(null=True)),
                ('prenda', models.CharField(max_length=300, null=True)),
                ('estado', models.IntegerField(default=0, editable=False, choices=[(0, b'Pendiente'), (1, b'En Proceso'), (2, b'En Produccion'), (3, b'Terminado'), (4, b'Revisado'), (5, b'Entregado'), (6, b'Rechazado')])),
                ('ninos', models.BooleanField(default=False, verbose_name=b'ni\xc3\xb1os')),
                ('express', models.BooleanField(default=False)),
                ('con_forro', models.BooleanField(default=False)),
                ('con_pedreria', models.BooleanField(default=False, verbose_name=b'con pedreria/encaje/lentejuela')),
                ('descuento', models.DecimalField(default=0, max_digits=15, decimal_places=2)),
                ('total', models.DecimalField(default=0, max_digits=15, decimal_places=2)),
                ('cliente', models.ForeignKey(to='clientes.Cliente')),
                ('modista', models.ForeignKey(to='funcionarios.Funcionario', null=True)),
            ],
            options={
                'permissions': (('ver_ot_todos', 'Puede ver la lista general de trabajos'), ('ver_ot_pendientes', 'Puede ver la lista de trabajos pendientes'), ('ver_ot_proceso', 'Puede ver la lista de trabajos en proceso'), ('ver_ot_produccion', 'Puede ver la lista de trabajos en produccion'), ('ver_ot_terminados', 'Puede ver la lista de trabajos terminados'), ('ver_ot_revisados', 'Puede ver la lista de trabajos revisados'), ('ver_ot_entregados', 'Puede ver la lista de trabajos entregados'), ('ver_ot_rechazados', 'Puede ver la lista de trabajos rechazados'), ('ver_ot_entregas', 'Puede ver la lista de Entregas Pendientes'), ('pasar_ot_proceso', 'Puede pasar el trabajo al estado en proceso'), ('pasar_ot_produccion', 'Puede pasar el trabajo al estado en produccion'), ('pasar_ot_terminado', 'Puede pasar el trabajo al estado terminado'), ('pasar_ot_revisado', 'Puede pasar el trabajo al estado revisado'), ('pasar_ot_entregado', 'Puede pasar el trabajo al estado entregado'), ('pasar_ot_rechazado', 'Puede pasar el trabajo al estado rechazado'), ('retroceder_ot_pendiente', 'Puede retroceder el trabajo al estado pendiente'), ('retroceder_ot_proceso', 'Puede retroceder el trabajo al estado en proceso'), ('retroceder_ot_produccion', 'Puede retroceder el trabajo al estado en produccion'), ('retroceder_ot_terminado', 'Puede retroceder el trabajo al estado terminado'), ('retroceder_ot_revisado', 'Puede retroceder el trabajo al estado revisado'), ('retroceder_ot_entregado', 'Puede retroceder el trabajo al estado entregado'), ('reprogramar_ot', 'Puede reprogramar el trabajo rechazado'), ('asignar_modista', 'Puede asignar una modista a la OT')),
            },
        ),
        migrations.AddField(
            model_name='detalleordendetrabajo',
            name='orden_de_trabajo',
            field=models.ForeignKey(to='produccion.OrdenDeTrabajo'),
        ),
        migrations.AddField(
            model_name='detalleordendetrabajo',
            name='servicio',
            field=models.ForeignKey(to='servicios.Servicio'),
        ),
        migrations.AddField(
            model_name='detalleordendetrabajo',
            name='tela',
            field=models.ForeignKey(to='servicios.Tela'),
        ),
    ]
