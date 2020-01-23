from __future__ import unicode_literals
from django import template
from django.contrib.admin.views.main import SEARCH_VAR
from django.contrib.admin.templatetags.admin_list import result_headers, result_hidden_fields, results

from retoqueria.globales import separar
from ventas.servicios import get_sesion_abierta

register = template.Library()

@register.filter()
def separate(numero,decimales=False):
    if numero:
        numero = not decimales and int(numero) or numero
        return separar(numero)
    return numero


def advanced_search_form(context, cl):
    """
    Displays a search form for searching the list.
    """
    form = context.get('asf')
    form = form(data=context.get('my_request_get'))
    return {
        'asf' : form,
        'cl': cl,
        'request':context.get('request',''),
        'panel':context.get('panel',''),
        'show_result_count': cl.result_count != cl.full_result_count,
        'search_var': SEARCH_VAR
    }


@register.inclusion_tag('admin/ventas/venta/venta_search_form.html', takes_context=True)
def venta_search_form(context, cl):
   return advanced_search_form(context, cl)


@register.inclusion_tag('admin/ventas/movimientoflujocaja/movimiento_flujocaja_search_form.html', takes_context=True)
def movimiento_flujocaja_search_form(context, cl):
   return advanced_search_form(context, cl)


@register.simple_tag(takes_context=True)
def caja_actual(context):
    sesion = get_sesion_abierta(context.get('user',''))

    return str(sesion.caja) if sesion else ''
