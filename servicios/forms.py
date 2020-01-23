from dal import autocomplete
from django import forms
from django.forms import CharField

from servicios.models import *


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ('__all__')
        widgets = {
            "categoria": autocomplete.ModelSelect2(url='categoriadeservicio-autocomplete'),
            "es_plantilla": forms.HiddenInput(),
            "servicio_padre": forms.HiddenInput(),
        }


class DetalleDeServicioTelaForm(forms.ModelForm):
    class Meta:
        model = DetalleDeServicioTela
        fields = ('__all__')
        widgets = {
            "tela": autocomplete.ModelSelect2(url='tela-autocomplete'),
            "precio": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }


class DetalleDeServicioMaterialForm(forms.ModelForm):
    class Meta:
        model = DetalleDeServicioMaterial
        fields = ('__all__')
        widgets = {
            "material": autocomplete.ModelSelect2(url='material-autocomplete'),
            "cantidad": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }
