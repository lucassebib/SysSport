from django import forms
#from novedades.models import Profesor, Alumno

#class FormularioProfesor(formsModelForm):
#	class Meta:
#		modelo = Profesor
#
#class FormularioAlumno(formsModelForm):
#	class Meta:
#		modelo = Alumno 

class FormularioAutenticacion(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'usuario'}))
	password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'placeholder': 'Password'}))