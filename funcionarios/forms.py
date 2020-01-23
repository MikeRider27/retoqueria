from django import forms
from dal import autocomplete
from funcionarios.models import Liquidacion, DetalleDeLiquidacion


class LiquidacionForm(forms.ModelForm):
    class Meta:
        model = Liquidacion
        fields = '__all__'
        widgets = {
            "modista": autocomplete.ModelSelect2(url='funcionario-autocomplete'),
            "total": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }


class DetalleDeLiquidacionForm(forms.ModelForm):
    class Meta:
        model = DetalleDeLiquidacion
        fields = '__all__'
        widgets = {
            "servicio": autocomplete.ModelSelect2(url='detalleordendetrabajo-autocomplete'),
            "subtotal": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }