from dal import autocomplete
from django import forms
from materiales.models import Material

class MaterialForm(forms.ModelForm):
	class Meta:
		model = Material
		fields = ('__all__')
		widgets = { 
			"unidad_de_medida": autocomplete.ModelSelect2(url='unidaddemedida-autocomplete'),
			"categoria": autocomplete.ModelSelect2(url='categoriadematerial-autocomplete'),
			"stock_minimo":forms.TextInput(attrs={'style':'text-align:right','size':'12','class':'auto','data-a-sep':'.','data-a-dec':','}),
		}

