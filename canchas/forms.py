from django import forms
from models import Cancha

class FormularioCrearCancha(forms.ModelForm):
	class Meta:
		model = Cancha
