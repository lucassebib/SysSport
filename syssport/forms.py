#-!-coding: utf-8 -!-
from django import forms
from django.db import models

from usuarios.models import Alumno

class FormularioAutenticacion(forms.Form):	
	username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'usuario', 'class':'form-control', 'required' :'True'}))
	password = forms.CharField(label='', widget=forms.PasswordInput(render_value=False, attrs={'placeholder': 'contraseña','class':'form-control', 'required':'True'}))

class FormularioRegistracion(forms.ModelForm):
	legajo = forms.CharField(label='legajo', widget=forms.NumberInput(attrs={'placeholder':'legajo', 'class':'form-control', 'required':'True'}))
	password = forms.CharField(label='contrasena', widget=forms.PasswordInput(render_value=False, attrs={'placeholder': 'contrasena','class':'form-control', 'required':'True'}))

	class Meta:
		model = Alumno
		fields = ["legajo", "password", "lista_deporte"]
		widgets = {
           'lista_deporte': forms.Select(attrs={'class':'form-control'})
        }