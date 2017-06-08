from django import forms
from models import Deporte, FichaMedica

class FormularioCrearDeporte(forms.ModelForm):
	class Meta:
		model = Deporte
		fields = ['nombre', 'descripcion', 'foto', 'apto_para']
		exclude=['ficha_medica']
		widgets = {
           'nombre':forms.TextInput(attrs={'required':'True'}),
           'descripcion': forms.Textarea(attrs={'required':'True'})
        }
		
class FormularioSubirFichaMedica(forms.ModelForm):
	class Meta:
		model = FichaMedica
				

class FormularioEditarDeporteProfesor(forms.ModelForm):
	class Meta:
	        model = Deporte
	        fields = ['foto', 'descripcion']
	        
