from django import forms
from models import Deporte

class FormularioCrearDeporte(forms.ModelForm):
	class Meta:
		model = Deporte
