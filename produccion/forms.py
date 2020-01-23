from __future__ import print_function
from dal import autocomplete
from django import forms
from django.core.exceptions import ValidationError

from extra.globals import separador_de_miles
from produccion.models import *
from servicios.models import Tela, DetalleDeServicioTela


from django.forms import formsets
from django.forms.models import BaseInlineFormSet


class OrdenDeTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenDeTrabajo
        exclude = ['modista', ]

        widgets = {
            "cliente": autocomplete.ModelSelect2(url='cliente-autocomplete'),
            "descuento": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto iterable', 'data-a-sep': '.',
                       'data-a-dec': ','}),
            "total": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }

    def __init__(self, *args, **kwargs):
        super(OrdenDeTrabajoForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if not (instance and instance.pk):
            self.initial['fecha_de_entrega'] = get_fecha_de_taller()
        self.fields['total'].widget.attrs['readonly'] = True
        self.fields['descuento'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super(OrdenDeTrabajoForm, self).clean()
        fecha_de_entrega = cleaned_data.get("fecha_de_entrega")
        dias_para_prueba = cleaned_data.get('dias_para_prueba')
        dias_post_prueba = cleaned_data.get('dias_post_prueba')
        orden_trabajo = self.instance if self.instance and self.instance.pk else None

        if not orden_trabajo:
            if dias_para_prueba and dias_post_prueba:
                fecha_calculada = date.today() + timedelta(days=(dias_para_prueba + dias_post_prueba))
            else:
                fecha_calculada = get_fecha_de_taller()

            if fecha_calculada > fecha_de_entrega:
                msg = 'Fecha Estimada "%s"'%fecha_calculada.strftime('%d/%m/%Y')
                self.add_error('fecha_de_entrega', msg)

        return cleaned_data


class DetalleOrdenDeTrabajoForm(forms.ModelForm):
    class Meta:
        model = DetalleOrdenDeTrabajo
        fields = ('__all__')

        widgets = {
            "categoria_servicio": autocomplete.ModelSelect2(url='categoriadeservicio-autocomplete'),
            "servicio": autocomplete.ModelSelect2(url='servicio-por-categoria-autocomplete', forward=['categoria_servicio']),
            "cantidad": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '6', 'class': 'auto iterable', 'data-a-sep': '.',
                       'data-a-dec': ','}),
            "precio": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto iterable', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }
    tela = forms.ModelChoiceField(
        queryset=Tela.objects.all(),
        widget=autocomplete.ModelSelect2(url='telaitem-autocomplete', forward=['servicio']),
        label="tela"
    )
    observaciones = forms.CharField(widget=forms.Textarea(attrs={'rows': '1', 'cols': '80'}), required=False)
    duracion = forms.IntegerField(required=False,
                              label='duracion en minutos',
                              widget=forms.TextInput(attrs={'readonly': 'readonly',
                                                            'style': 'text-align:right;width:100px;'}))

    def __init__(self, **kwargs):
        super(DetalleOrdenDeTrabajoForm, self).__init__(**kwargs)
        if self.instance and self.instance.pk:
            self.fields['duracion'].initial = self.instance.servicio.duracion
        else:
            self.fields['duracion'].initial = 0


class AsignarModistaForm(forms.ModelForm):
    class Meta:
        model = OrdenDeTrabajo
        fields = ('modista',)
        widgets = {
            "modista": autocomplete.ModelSelect2(url='funcionario-autocomplete'),
        }


ETAPAS_CHOICES = (
    (OT_PENDIENTE, 'Pendiente'),
    (OT_PROCESO, 'En Proceso'),
    (OT_PRODUCCION, 'En Produccion'),
    (OT_TERMINADO, 'Terminado'),
    (OT_REVISADO, 'Revisado'),
    (OT_ENTREGADO, 'Entregado'),
)


class ReprogramarTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenDeTrabajo
        fields = ('modista', 'fecha_de_entrega',)
        widgets = {
            "modista": autocomplete.ModelSelect2(url='funcionario-autocomplete'),
        }

    etapa = forms.IntegerField(
        widget=forms.Select(choices=ETAPAS_CHOICES),
        label="Tela",
        required=True
    )

    def save(self, commit=True):
        detalle = super(ReprogramarTrabajoForm, self).save(commit=False)
        detalle.revision = detalle.revision + 1
        detalle.estado = self.cleaned_data.get('etapa')

        if commit:
            detalle.save()
        return detalle

