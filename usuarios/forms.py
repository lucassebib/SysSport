from django import forms
from django.forms import ClearableFileInput
from models import Alumno, Direccion, ContactoDeUrgencia, Persona, UsuarioInvitado, DatosMedicos, Profesor
from django.db import models

class FormularioAutenticacion(forms.Form):	
	username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'usuario', 'class':'form-control', 'required' :'True'}))
	password = forms.CharField(label='', widget=forms.PasswordInput(render_value=False, attrs={'placeholder': 'contrasena','class':'form-control', 'required':'True'}))

class FormularioRegistracion(forms.ModelForm):
	legajo = forms.CharField(label='legajo', widget=forms.TextInput(attrs={'placeholder':'legajo', 'class':'form-control', 'required':'True'}))
	password = forms.CharField(label='contrasena', widget=forms.PasswordInput(render_value=False, attrs={'placeholder': 'contrasena','class':'form-control', 'required':'True'}))

	class Meta:
		model = Alumno
		fields = ["legajo", "password", "lista_deporte"]
		widgets = {
           'lista_deporte': forms.Select(attrs={'class':'form-control'})
        }

class FormularioDireccion(forms.ModelForm):
	class Meta:
		model = Direccion

class FormularioContactoDeUrgencia(forms.ModelForm):
	class Meta:
		model = ContactoDeUrgencia

	def __init__(self, *args, **kwargs):
    		super(FormularioContactoDeUrgencia, self).__init__(*args, **kwargs)
    		self.fields['nombre'].required = True
    		self.fields['apellido'].required = True 
    		self.fields['parentezco'].required = True 
    		self.fields['telefono'].required = True  

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

class FormularioDatosMedicos(forms.ModelForm):
	class Meta:
		model = DatosMedicos

class FormularioAltaProfe(forms.ModelForm):
	class Meta:
		model = Profesor
		fields = ['username', 'password', 'first_name', 'last_name', 'dni','fecha_nacimiento','sexo','foto_perfil','email']


class FormularioEditarProfesor(forms.ModelForm):
	class Meta:
	        model = Profesor
	        fields = ['username', 'password', 'first_name', 'last_name','dni','fecha_nacimiento','sexo','foto_perfil','email' ]


class FormularioAltaAlumnoInvitado(forms.ModelForm):
	class Meta:
		model = UsuarioInvitado
		fields = ['username', 'password', 'first_name', 'last_name','dni','fecha_nacimiento','sexo','foto_perfil','email' ]


class FormularioEditarAlumnoInvitado(forms.ModelForm):
	class Meta:
	        model = UsuarioInvitado
	        fields = ['username', 'password', 'first_name', 'last_name','dni','fecha_nacimiento','sexo','foto_perfil','email' ]





