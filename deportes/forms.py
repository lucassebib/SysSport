from django import forms
from models import FichaMedica

#class FormularioCrearDeporte(forms.ModelForm):
#	class Meta:
#		model = Novedades

class FormularioSubirFichaMedica(forms.ModelForm):
	class Meta:
		model = FichaMedica