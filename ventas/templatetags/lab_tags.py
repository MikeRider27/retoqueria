from __future__ import unicode_literals
from django import template

from retoqueria.globales import separar
from ventas.lista_movimientos import advanced_search_form
from ventas.servicios import get_sesion_abierta

register = template.Library()


@register.filter()
def separate(numero, decimales=False):
    if numero:
        numero = not decimales and int(numero) or numero
        return separar(numero)
    return numero


@register.inclusion_tag('movimiento_flujocaja_search_form.html', takes_context=True)
def movimiento_flujocaja_search_form(context, cl):
   return advanced_search_form(context, cl)


@register.simple_tag(takes_context=True)
def caja_actual(context):
    sesion = get_sesion_abierta(context.get('user', ''))
    return str(sesion.caja) if sesion else ''
