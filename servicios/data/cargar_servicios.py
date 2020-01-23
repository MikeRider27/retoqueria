import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'retoqueria.settings'
import django

django.setup()

from servicios.models import CategoriaDeServicio, Servicio, DetalleDeServicioTela, Tela

import csv

Tela.objects.all().delete()

tela_fina = Tela.objects.create(nombre='Tela Fina')
jeans = Tela.objects.create(nombre='Jeans')
cuero_gamuza = Tela.objects.create(nombre='Cuero o Gamuza')
ninguna = Tela.objects.create(nombre='Ninguna')
fiesta = Tela.objects.create(nombre='De Fiesta')



CategoriaDeServicio.objects.all().delete()

archivo = 'servicios.csv'
with open(archivo) as csvfile:
    reader = csv.DictReader(csvfile)
    error_file = open('error_%s.log'%archivo,'w')
    j = 1
    for i, row in enumerate(reader):
        print (row)
        categoria,creado = CategoriaDeServicio.objects.get_or_create(codigo=row['codigo'],nombre=row['categoria'])

        j = (j+1) if not creado else 1
        servicio = Servicio.objects.create(
            descripcion=row['servicio'],
            codigo=row['codigo']+'.'+str(j),
            categoria=categoria
        )

        if int(row['tela_fina']) > 0:
            DetalleDeServicioTela.objects.create(
                servicio=servicio,
                tela=tela_fina,
                precio=row['tela_fina']
            )

        if int(row['jeans']) > 0:
            DetalleDeServicioTela.objects.create(
                servicio=servicio,
                tela=jeans,
                precio=row['jeans']
            )

        if int(row['cuero_gamuza']) > 0:
            DetalleDeServicioTela.objects.create(
                servicio=servicio,
                tela=cuero_gamuza,
                precio=row['cuero_gamuza']
            )


        if int(row['ninguna']) > 0:
            DetalleDeServicioTela.objects.create(
                servicio=servicio,
                tela=ninguna,
                precio=row['ninguna']
            )

        if int(row['fiesta']) > 0:
            DetalleDeServicioTela.objects.create(
                servicio=servicio,
                tela=fiesta,
                precio=row['fiesta']
            )

    error_file.close()

