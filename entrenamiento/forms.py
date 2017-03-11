from django import forms
from models import Entrenamiento

class FormularioCrearEntrenamiento(forms.ModelForm):
	class Meta:
		model = Entrenamiento