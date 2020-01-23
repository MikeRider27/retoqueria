from dal import autocomplete
from django import forms

from depositos.models import *
from materiales.models import Material
from produccion.models import OrdenDeTrabajo

class AltaForm(forms.ModelForm):
    class Meta:
        model = Alta
        fields = ('__all__')
        widgets = {
        	"funcionario": autocomplete.ModelSelect2(url='funcionario-autocomplete'),
        }


class DetalleAltaForm(forms.ModelForm):
    class Meta:
        model = DetalleAlta
        fields = ('__all__')
        widgets = {
        	"material": autocomplete.ModelSelect2(url='material-autocomplete'),
            "cantidad": forms.TextInput(attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.','data-a-dec': ','}),
        }

class BajaForm(forms.ModelForm):
    class Meta:
        model = Baja
        fields = ('__all__')
        widgets = {
        	"funcionario": autocomplete.ModelSelect2(url='funcionario-autocomplete'),
        }

class DetalleBajaForm(forms.ModelForm):
    class Meta:
        model = DetalleBaja
        fields = ('__all__')
        widgets = {
        	"material": autocomplete.ModelSelect2(url='material-autocomplete'),
            "cantidad": forms.TextInput(attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.','data-a-dec': ','}),
        }

class RetiroForm(forms.ModelForm):
    class Meta:
        model = Retiro
        fields = ('__all__')
        widgets = {
        	"funcionario": autocomplete.ModelSelect2(url='funcionario-autocomplete'),
        }

class DetalleRetiroForm(forms.ModelForm):
    class Meta:
        model = DetalleRetiro
        fields = ('__all__')
        widgets = {
            "detalle_orden_de_trabajo": autocomplete.ModelSelect2(url='detalleordendetrabajo-autocomplete'),
        	"material": autocomplete.ModelSelect2(url='material-autocomplete'),
            "cantidad": forms.TextInput(attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.','data-a-dec': ','}),
        }


class DevolucionForm(forms.ModelForm):
    class Meta:
        model = Devolucion
        fields = ('__all__')
        widgets = {
        	"funcionario": autocomplete.ModelSelect2(url='funcionario-autocomplete'),
        }

    retiro = forms.ModelChoiceField(
        queryset=Retiro.objects.all(),
        widget=autocomplete.ModelSelect2(url='retiro-autocomplete'),
        label="Retiro"
    )

class DetalleDevolucionForm(forms.ModelForm):
    class Meta:
        model = DetalleDevolucion
        fields = ('__all__')
        widgets = {
            "detalle_retiro": autocomplete.ModelSelect2(url='detalleretiro-autocomplete', forward=['retiro']),
            "cantidad": forms.TextInput(attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.','data-a-dec': ','}),
        }




