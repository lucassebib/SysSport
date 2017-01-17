from django import forms
from models import Novedades

class FormularioCrearDeporte(forms.ModelForm):
	class Meta:
		model = Novedades
