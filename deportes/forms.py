from django import forms
from models import Deporte, FichaMedica

class FormularioCrearDeporte(forms.ModelForm):
	class Meta:
		model = Deporte

class FormularioSubirFichaMedica(forms.ModelForm):
	class Meta:
		model = FichaMedica

class FormularioEditarDeporteProfesor(forms.ModelForm):
	class Meta:
	        model = Deporte
	        fields = ["descripcion" ,"foto"]
