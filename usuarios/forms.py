from django import forms
from models import Alumno, Direccion, ContactoDeUrgencia
from django.db import models

class FormularioAutenticacion(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'usuario'}))
	password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'placeholder': 'Password'}))

class FormularioDireccion(forms.ModelForm):
	class Meta:
		model = Direccion

class FormularioContactoDeUrgencia(forms.ModelForm):

	class Meta:
		model = ContactoDeUrgencia


	






