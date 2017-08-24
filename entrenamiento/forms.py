from django import forms
from models import Entrenamiento

class FormularioCrearEntrenamiento(forms.ModelForm):
	hora_inicio = forms.CharField( widget=forms.TextInput(attrs={'type': 'time'}) )
	hora_fin = forms.CharField( widget=forms.TextInput(attrs={'type': 'time'}) )

	class Meta:
		model = Entrenamiento
		fields = ["dia"]