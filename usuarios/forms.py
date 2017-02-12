from django import forms
from models import Alumno, Direccion, ContactoDeUrgencia
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


	






