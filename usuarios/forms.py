from django import forms
from django.forms import ClearableFileInput
from models import Alumno, Direccion, ContactoDeUrgencia, Persona, UsuarioInvitado
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

class FormularioCargarArchivo(forms.ModelForm):
	class Meta:
	        model = Alumno
	        fields = ["ficha_medica"]

class FormularioEdicionPerfilInvitado(forms.ModelForm):
	class Meta:
		model = UsuarioInvitado
		exclude = ['username', 'password', 'groups','user_permissions', 'is_staff', 'is_active', 'is_superuser', 
		'last_login', 'date_joined', 'foto_perfil', 'lista_deporte', 'sexo', 'direccion', 'institucion', 
		'ficha_medica', 'contactos_de_urgencia']

	






