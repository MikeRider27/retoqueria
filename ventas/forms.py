from dal import autocomplete
from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from clientes.models import Cliente
from ventas.models import *


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'

        widgets = {
            "cliente": autocomplete.ModelSelect2(url='cliente-autocomplete'),
            "total": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ('__all__')

        widgets = {
            "orden_de_trabajo": autocomplete.ModelSelect2(url='ordendetrabajo_venta-autocomplete', forward=['cliente']),
            "precio": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }


class MovimientoFlujoCajaForm(forms.Form):
    caja = forms.ModelChoiceField(
        queryset=Caja.objects.all(),
        widget=autocomplete.ModelSelect2(url='caja-autocomplete',), required=False
    )
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        widget=autocomplete.ModelSelect2(url='cliente-autocomplete', ), required=False
    )
    desde = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Desde'}), required=False)
    hasta = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Hasta'}), required=False, initial=datetime.now())


class CierreCajaForm(forms.ModelForm):
    class Meta:
        model = CierreCaja
        fields = '__all__'

    class Media:
        js = (
            '/static/admin/js/autoNumeric.js',
            '/static/admin/cierre_caja/cierre_caja.js',

        )
        css = {
            'all': ('/static/admin/movimiento/movimiento_caja.css',)
        }
    ingresos = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'auto', 'style': 'text-align: right'}))
    egresos = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'auto', 'style': 'text-align: right'}))
    saldo_cierre = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'auto', 'style': 'text-align: right'}))
    saldo_apertura = forms.CharField(required=False,
                                     widget=forms.TextInput(
                                         attrs={'readonly': 'readonly', 'class':'auto', 'style': 'text-align: right'}))

    def __init__(self,*args,**kwargs):
        super(CierreCajaForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['ingresos'].initial = self.instance.total_ingresos()
            self.fields['egresos'].initial = self.instance.total_egresos()
            self.fields['saldo_cierre'].initial = self.instance.get_saldo_cierre()