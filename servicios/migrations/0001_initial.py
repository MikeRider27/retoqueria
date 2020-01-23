# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaDeServicio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.IntegerField(default=0)),
                ('nombre', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'categoria de servicio',
                'verbose_name_plural': 'categorias de servicio',
            },
        ),
        migrations.CreateModel(
            name='DetalleDeServicioMaterial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.DecimalField(max_digits=15, decimal_places=2)),
                ('material', models.ForeignKey(to='materiales.Material')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleDeServicioTela',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('precio', models.DecimalField(max_digits=15, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=10)),
                ('descripcion', models.CharField(max_length=100)),
                ('duracion', models.IntegerField(default=0, verbose_name=b'duracion (en minutos)')),
                ('es_plantilla', models.BooleanField(default=True)),
                ('categoria', models.ForeignKey(to='servicios.CategoriaDeServicio')),
                ('servicio_padre', models.ForeignKey(blank=True, to='servicios.Servicio', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tela',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='detalledeserviciotela',
            name='servicio',
            field=models.ForeignKey(to='servicios.Servicio'),
        ),
        migrations.AddField(
            model_name='detalledeserviciotela',
            name='tela',
            field=models.ForeignKey(to='servicios.Tela'),
        ),
        migrations.AddField(
            model_name='detalledeserviciomaterial',
            name='servicio',
            field=models.ForeignKey(to='servicios.Servicio'),
        ),
    ]
