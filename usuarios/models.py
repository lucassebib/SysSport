from django.db import models
from django.contrib.auth.models import User as Usuario
from deportes.models import Deporte
from django.contrib import admin

class Persona(Usuario):
	#Hereda de Usuario> 'username', 'password', 'first_name', 'last_name', 'groups', 'user_permissions', 
	#'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined'
	dni = models.IntegerField()
	fecha_nacimiento = models.DateField()
	telefono = models.IntegerField()
	foto_perfil = models.ImageField(upload_to='fotos_de_perfil/', blank=True, null=True)
	lista_deporte = models.ManyToManyField(Deporte, verbose_name='Deportes Inscripto')

class Profesor(Persona):
	legajo =  models.IntegerField()

	class Meta:
		verbose_name_plural = "Profesores"

	#def __unicode__(self):
	#	return '%s %s' % (self.nombre, self.apellido)

	def tipo_usuario(self, cadena):
		return cadena == 'profesor'

	def profesor_de(self):
		return "\n -".join([d.nombre for d in self.lista_deporte.all()])

class Alumno(Persona):
	carreras_disponibles = ((1,"ISI"),(2,"IQ"), (3, "IEM"), (4, "LAR"), (5, "TSP"))

	legajo =  models.IntegerField()
	ficha_medica = models.FileField(upload_to='fichas_medicas/', blank=True)
	carrera = models.IntegerField(choices=carreras_disponibles, default=1)

	class Meta:
		verbose_name_plural = "Alumnos"

	def obtener_deportes(self):
		lista = self.lista_deporte.all()
		return lista

	def deportes_inscripto(self):
		return "\n -".join([d.nombre for d in self.lista_deporte.all()])

	def tipo_usuario(self, cadena):
		return cadena == 'alumno'

class UsuarioInvitado(Persona): 
	institucion = models.CharField(max_length=100)
	ficha_medica = models.FileField(upload_to='fichas_medicas/', blank=True)

	class Meta:
		verbose_name_plural = "UsuariosInvitados"

	def obtener_deportes(self):
		lista = self.lista_deporte.all()
		return lista

	def deportes_inscripto(self):
		return "\n -".join([d.nombre for d in self.lista_deporte.all()])

	def tipo_usuario(self, cadena):
		return cadena=='invitado'

##################AGREGAMOS CLASES AL PANEL DE ADMINISTRACION##################################

class ProfesorAdmin(admin.ModelAdmin):
	list_display = ('legajo','dni','fecha_nacimiento','telefono','email','profesor_de')
	fields = ('username', 'password', 'first_name', 'last_name', 'legajo', 'dni', 'fecha_nacimiento', 'telefono', 'foto_perfil', 'lista_deporte')

admin.site.register(Profesor,ProfesorAdmin)

class AlumnoAdmin(admin.ModelAdmin):
	list_display = ('legajo', 'deportes_inscripto')
	fields = ('username', 'password', 'first_name', 'last_name', 'carrera', 'legajo', 'dni', 'fecha_nacimiento', 'telefono', 'foto_perfil', 'lista_deporte', 'ficha_medica', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')

admin.site.register(Alumno,AlumnoAdmin)

class UsuarioInvitadoAdmin(admin.ModelAdmin):
	list_display = ('institucion', 'deportes_inscripto')
	fields = ('username', 'password', 'first_name', 'last_name', 'dni', 'institucion' , 'fecha_nacimiento', 'telefono', 'foto_perfil', 'lista_deporte', 'ficha_medica', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')

admin.site.register(UsuarioInvitado,UsuarioInvitadoAdmin)