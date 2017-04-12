from django import forms
from django.forms import ClearableFileInput, TextInput
from django.contrib.admin.widgets import AdminDateWidget 
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
		'ficha_medica', 'contactos_de_urgencia', 'datos_medicos']

class FormularioDatosMedicos(forms.ModelForm):
	class Meta:
		model = DatosMedicos

################## AMB usuarios##############################

class FormularioAltaProfe(forms.ModelForm):
	password2 = forms.CharField(label='confirmar password:', widget=forms.PasswordInput(render_value=False, attrs={'required':'True'}))
	class Meta:		
		model = Profesor
		widgets = {
			'username':forms.TextInput(attrs={'required':'True'}),
			'password': forms.PasswordInput(render_value=False, attrs={'required':'True'}),
			'first_name':forms.TextInput(attrs={'size': 30,}),
			'last_name':forms.TextInput(attrs={'size': 30, 'required':'True'}),
			'fecha_nacimiento':AdminDateWidget(attrs={'required':'True'}),
			'email':forms.TextInput(attrs={'size':30, 'placeholder':'suemail@gmail.com', 'requiered':'True'}),
			'telefono':forms.TextInput(attrs={'placeholder':'3624787542'}),
			'dni':forms.TextInput(attrs={'placeholder':'34954568'}),
			'telefono':forms.TextInput(attrs={'placeholder':'3624787542', 'requiered':'True'}),
			'lista_deporte': forms.CheckboxSelectMultiple(),
        }
 
  		fields = ['username', 'password', 'first_name', 'last_name', 'dni','fecha_nacimiento','sexo','foto_perfil','email','telefono','lista_deporte']
  	



class FormularioEditarProfesor(forms.ModelForm):
	password2 = forms.CharField(label='confirmar password', widget=forms.PasswordInput(render_value=False, attrs={'required':'False'}))
	class Meta:		
		model = Profesor
		widgets = {
			'username':forms.TextInput(attrs={'required':'True'}),
			'password': forms.PasswordInput(render_value=False, attrs={'required':'False'}),
			'first_name':forms.TextInput(attrs={'size': 30,}),
			'last_name':forms.TextInput(attrs={'size': 30, 'required':'True'}),
			'fecha_nacimiento':AdminDateWidget(attrs={'required':'True'}),
			'email':forms.TextInput(attrs={'size':30, 'placeholder':'suemail@gmail.com', 'requiered':'True'}),
			'telefono':forms.TextInput(attrs={'placeholder':'3624787542'}),
			'dni':forms.TextInput(attrs={'placeholder':'34954568'}),
			'telefono':forms.TextInput(attrs={'placeholder':'3624787542', 'requiered':'True'}),
			'lista_deporte': forms.CheckboxSelectMultiple(),
        }


		fields = ['username', 'password', 'first_name', 'last_name','dni','fecha_nacimiento','sexo','foto_perfil','email','telefono','lista_deporte' ]




class FormularioAltaAlumnoInvitado(forms.ModelForm):
	password2 = forms.CharField(label='', widget=forms.PasswordInput(render_value=False, attrs={'required':'True'}))
	class Meta:
		model = UsuarioInvitado
		widgets = {
			'username':forms.TextInput(attrs={'required':'True'}),
			'password': forms.PasswordInput(render_value=False, attrs={'required':'True'}),
			'first_name':forms.TextInput(attrs={'size': 30,}),
			'last_name':forms.TextInput(attrs={'size': 30, 'required':'True'}),
			'fecha_nacimiento':AdminDateWidget(attrs={'required':'True'}),
			'email':forms.TextInput(attrs={'size':30, 'placeholder':'suemail@gmail.com', 'requiered':'True'}),
			'telefono':forms.TextInput(attrs={'placeholder':'3624787542'}),
			'dni':forms.TextInput(attrs={'placeholder':'34954568'}),
			'telefono':forms.TextInput(attrs={'placeholder':'3624787542', 'requiered':'True'}),
			'lista_deporte': forms.CheckboxSelectMultiple(),
			
        }

		fields = ['username', 'password', 'first_name', 'last_name','dni','fecha_nacimiento','sexo','foto_perfil','email','telefono', 'lista_deporte' ]




class FormularioEditarAlumnoInvitado(forms.ModelForm):	
	password2 = forms.CharField(label='', widget=forms.PasswordInput(render_value=False, attrs={'required':'False'}))
	class Meta:
		model = Profesor
		widgets = {
			'username':forms.TextInput(attrs={'required':'True'}),
			'password': forms.PasswordInput(render_value=False, attrs={'required':'False'}),
			'first_name':forms.TextInput(attrs={'size': 30,}),
			'last_name':forms.TextInput(attrs={'size': 30, 'required':'True'}),
			'fecha_nacimiento':AdminDateWidget(attrs={'required':'True'}),
			'email':forms.TextInput(attrs={'size':30, 'placeholder':'suemail@gmail.com', 'requiered':'True'}),
			'telefono':forms.TextInput(attrs={'placeholder':'3624787542'}),
			'dni':forms.TextInput(attrs={'placeholder':'34954568'}),
			'telefono':forms.TextInput(attrs={'placeholder':'3624787542', 'requiered':'True'}),
			'lista_deporte': forms.CheckboxSelectMultiple(),
        }


		fields = ['username', 'password', 'first_name', 'last_name','dni','fecha_nacimiento','sexo','foto_perfil','email','telefono','lista_deporte' ]
