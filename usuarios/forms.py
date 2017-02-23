from django import forms
from django.forms import ClearableFileInput
from models import Alumno, Direccion, ContactoDeUrgencia, Persona
from django.db import models

class FormularioAutenticacion(forms.Form):	
	username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'usuario', 'class':'form-control', 'required' :'True'}))
	password = forms.CharField(label='', widget=forms.PasswordInput(render_value=False, attrs={'placeholder': 'contrasena','class':'form-control', 'required':'True'}))

class FormularioDireccion(forms.ModelForm):
	class Meta:
		model = Direccion

class FormularioContactoDeUrgencia(forms.ModelForm):
	class Meta:
		model = ContactoDeUrgencia

class FormularioCargarImagen(forms.ModelForm):
	class Meta:
		model = Persona
		fields = ["foto_perfil"]

#class CustomClearableFileInput(ClearableFileInput):
#    template_with_clear = '<br>  <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label> %(clear)s'

#class FormularioCargarArchivo(forms.ModelForm):
#	class Meta:
#	        model = Alumno
#	        fields = ["ficha_medica"]
#	        widgets = {
#	            'ficha_medica': CustomClearableFileInput
#	        }	

	






