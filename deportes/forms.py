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
	        fields = ["foto", "descripcion"]
	        descripcion = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows':'20'}))
