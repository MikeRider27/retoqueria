# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('funcionarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='Baja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='Deposito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleAlta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.DecimalField(max_digits=15, decimal_places=2)),
                ('motivo', models.CharField(max_length=500, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleBaja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.DecimalField(max_digits=15, decimal_places=2)),
                ('motivo', models.CharField(max_length=500, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleDevolucion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.DecimalField(max_digits=15, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleRetiro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.DecimalField(max_digits=15, decimal_places=2)),
                ('deposito', models.ForeignKey(to='depositos.Deposito')),
            ],
        ),
        migrations.CreateModel(
            name='Devolucion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('funcionario', models.ForeignKey(to='funcionarios.Funcionario')),
            ],
        ),
        migrations.CreateModel(
            name='Retiro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('funcionario', models.ForeignKey(to='funcionarios.Funcionario')),
            ],
        ),
        migrations.AddField(
            model_name='devolucion',
            name='retiro',
            field=models.ForeignKey(to='depositos.Retiro', null=True),
        ),
    ]
