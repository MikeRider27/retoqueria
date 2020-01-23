import json
from django.http import HttpResponse
from produccion.models import *
from extra.globals import separador_de_miles
from django.http.response import JsonResponse
from produccion.models import DetalleOrdenDeTrabajo


def get_ordendetrabajo(request):
    orden_de_trabajo_id = (request.GET['otid']).replace(" ","")

    result_set = []

    if orden_de_trabajo_id == "":
        return HttpResponse(json.dumps(result_set), 
                            content_type='application/json')

    orden_de_trabajo = OrdenDeTrabajo.objects.get(pk = orden_de_trabajo_id)

    result_set.append({
        'numero': separador_de_miles(orden_de_trabajo.id),
        'prenda': orden_de_trabajo.prenda,
        'total': separador_de_miles(orden_de_trabajo.total),

    })

    return HttpResponse(json.dumps(result_set), 
                        content_type='application/json')


def get_detalle_ot_duracion(request):
    detalle_id = request.GET.get('detalle_ot_id', '')
    if not detalle_id:
        return HttpResponse(json.dumps([]),
                            content_type='application/json')
    detalle = DetalleOrdenDeTrabajo.objects.get(pk=detalle_id)
    return HttpResponse(json.dumps({'duracion': detalle.servicio.duracion}),
                        content_type='application/json')