import json
from django.http import HttpResponse
from servicios.models import *
from extra.globals import *

def get_servicio(request):
    servicio_id = (request.GET['servicioid']).replace(" ","")

    result_set = []

    if servicio_id == "":
        return HttpResponse(json.dumps(result_set), 
                            content_type='application/json')

    servicio = Servicio.objects.get(pk = servicio_id)

    result_set.append({
        'codigo': servicio.codigo,
        'descripcion': servicio.descripcion,
        'duracion': servicio.duracion,
        'es_plantilla': servicio.es_plantilla
    })

    return HttpResponse(json.dumps(result_set), 
                        content_type='application/json')


def get_lista_de_telas_del_servicio(request):
    servicio_id = (request.GET['servicioid']).replace(" ","")

    result_set = []

    if servicio_id == "":
        return HttpResponse(json.dumps(result_set), 
                            content_type='application/json')

    detalles = DetalleDeServicioTela.objects.filter(servicio_id = servicio_id)

    for detalle in detalles:
        result_set.append({
            'id': detalle.tela.id,
            'tela': unicode(detalle.tela.nombre),
            'precio': separador_de_miles(detalle.precio),
        })

    return HttpResponse(json.dumps(result_set), 
                        content_type='application/json')

def get_lista_de_materiales_del_servicio(request):
    servicio_id = (request.GET['servicioid']).replace(" ","")

    result_set = []

    if servicio_id == "":
        return HttpResponse(json.dumps(result_set), 
                            content_type='application/json')

    detalles = DetalleDeServicioMaterial.objects.filter(servicio_id = servicio_id)

    for detalle in detalles:
        result_set.append({
            'id': detalle.material.id,
            'material': unicode(detalle.material.descripcion),
            'cantidad': separador_de_miles(detalle.cantidad),
        })


    return HttpResponse(json.dumps(result_set), 
                        content_type='application/json')



def get_precio_del_servicio(request):
    servicio_id = (request.GET['servicioid']).replace(" ","")
    tela_id = (request.GET['telaid']).replace(" ","")

    result_set = []

    if servicio_id == "":
        return HttpResponse(json.dumps(result_set), 
                            content_type='application/json')

    if tela_id == "":
        return HttpResponse(json.dumps(result_set), 
                            content_type='application/json')

    detalles = DetalleDeServicioTela.objects.filter(servicio_id=servicio_id, tela_id=tela_id)

    for detalle in detalles:
        result_set.append({
            'precio': separador_de_miles(detalle.precio),
        })

    return HttpResponse(json.dumps(result_set), 
                        content_type='application/json')


def get_duracion_servicio(request):
    servicio_id = request.GET.get('servicio_id','')
    if not servicio_id:
        return HttpResponse(json.dumps({}),
                            content_type='application/json')
    servicio = Servicio.objects.get(pk=servicio_id)
    return HttpResponse(json.dumps({'duracion':servicio.duracion}),
                        content_type='application/json')