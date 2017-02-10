from django.db import models
from django.contrib.auth.models import User as Usuario
from deportes.models import Deporte
from django.contrib import admin
from .validators import valid_extension

class Direccion(models.Model):
	calle = models.CharField(max_length=100, blank=True, null=True)
	altura = models.IntegerField(blank=True, null=True)
	piso = models.IntegerField(blank=True, null=True)
	nro_departamento = models.IntegerField(blank=True, null=True)
	provincia = models.CharField(max_length=100, blank=True, null=True)
	localidad = models.CharField(max_length=100, blank=True, null=True)

	class Meta:
		verbose_name_plural = "Direcciones"

	def __unicode__(self):
		return '%s %s' % (self.calle, self.altura)

class ContactoDeUrgencia(models.Model):
	nombre = models.CharField(max_length=100, blank=True, null=True)
	apellido = models.CharField(max_length=100, blank=True, null=True)
	parentezco = models.CharField(max_length=100, blank=True, null=True)
	direccion = models.ForeignKey(Direccion, blank=True, null=True)
	telefono = models.IntegerField(blank=True, null=True)

class Persona(Usuario):
	lista_sexos = ((1,"Masculino"),(2,"Femenino"))

	#Hereda de Usuario> 'username', 'password', 'first_name', 'last_name', 'groups', 'user_permissions', 
	#'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined'
	dni = models.IntegerField(blank=True, null=True)
	fecha_nacimiento = models.DateField(blank=True, null=True)
	telefono = models.IntegerField(blank=True, null=True)
	foto_perfil = models.ImageField(upload_to='fotos_de_perfil/', default='default_profile.jpg', blank=True, null=True)
	lista_deporte = models.ManyToManyField(Deporte, verbose_name='Deportes Inscripto')
	direccion = models.ForeignKey(Direccion, blank=True, null=True)
	sexo = models.IntegerField(choices=lista_sexos, default=1)

	def obtenerNombreCompleto(self):
		return '%s %s' % (self.first_name, self.last_name)

	
	def ver_sexo(self):
		return self.get_sexo_display()

class Profesor(Persona):
	legajo =  models.IntegerField(blank=True, null=True)

	class Meta:
		verbose_name_plural = "Profesores"

	#def __unicode__(self):
	#	return '%s %s' % (self.nombre, self.apellido)

	def tipo_usuario(self, cadena):
		return cadena == 'profesor'

	def tipo_usuario(self):
		return 'profesor'

	def profesor_de(self):
		return "\n -".join([d.nombre for d in self.lista_deporte.all()])

class Alumno(Persona):
	carreras_disponibles = ((1,"ISI"),(2,"IQ"), (3, "IEM"), (4, "LAR"), (5, "TSP"))

	legajo =  models.IntegerField(blank=True, null=True)
	ficha_medica = models.FileField(upload_to='fichas_medicas/', blank=True, validators=[valid_extension])
	carrera = models.IntegerField(choices=carreras_disponibles, default=1)
	contactos_de_urgencia = models.ManyToManyField(ContactoDeUrgencia, verbose_name='Contacto de Urgencia', blank=True, null=True)

	class Meta:
		verbose_name_plural = "Alumnos"

	def obtener_deportes(self):
		lista = self.lista_deporte.all()
		return lista

	def deportes_inscripto(self):
		return "\n -".join([d.nombre for d in self.lista_deporte.all()])

	def tipo_usuario(self, cadena):
		return cadena == 'alumno'

	def tipo_usuario(self):
		return 'alumno'

	def ver_nombre_carrera(self):
		return self.get_carrera_display()
		
class UsuarioInvitado(Persona): 
	institucion = models.CharField(max_length=100)
	ficha_medica = models.FileField(upload_to='fichas_medicas/', blank=True)
	contactos_de_urgencia = models.ManyToManyField(ContactoDeUrgencia, verbose_name='Contacto de Urgencia', blank=True, null=True)

	class Meta:
		verbose_name_plural = "Usuarios Invitados"

	def obtener_deportes(self):
		lista = self.lista_deporte.all()
		return lista

	def deportes_inscripto(self):
		return "\n -".join([d.nombre for d in self.lista_deporte.all()])

	def tipo_usuario(self, cadena):
		return cadena=='invitado'

	def tipo_usuario(self):
		return 'invitado'

##################AGREGAMOS CLASES AL PANEL DE ADMINISTRACION##################################

class ProfesorAdmin(admin.ModelAdmin):
	list_display = ('legajo','dni','fecha_nacimiento','telefono','email','profesor_de')
	fields = ('username', 'password','sexo', 'first_name', 'last_name', 'direccion', 'legajo', 'dni', 'fecha_nacimiento', 'telefono', 'foto_perfil', 'lista_deporte')

admin.site.register(Profesor,ProfesorAdmin)

class AlumnoAdmin(admin.ModelAdmin):
	list_display = ('legajo', 'deportes_inscripto')
	fields = ('username', 'password', 'first_name', 'last_name','sexo', 'direccion', 'carrera', 'legajo', 'dni', 'fecha_nacimiento', 'telefono', 'foto_perfil', 'lista_deporte', 'ficha_medica','contactos_de_urgencia', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')

admin.site.register(Alumno,AlumnoAdmin)

class UsuarioInvitadoAdmin(admin.ModelAdmin):
	list_display = ('institucion', 'deportes_inscripto')
	fields = ('username', 'password', 'first_name', 'last_name', 'dni', 'sexo','institucion' , 'fecha_nacimiento', 'telefono', 'foto_perfil', 'lista_deporte', 'ficha_medica', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')

admin.site.register(UsuarioInvitado,UsuarioInvitadoAdmin)

class DireccionAdmin(admin.ModelAdmin):
	list_display = ('calle', 'altura', 'piso', 'nro_departamento', 'provincia', 'localidad')

admin.site.register(Direccion,DireccionAdmin)

class ContactoUrgenciaAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'apellido', 'parentezco', 'direccion', 'telefono')

admin.site.register(ContactoDeUrgencia,ContactoUrgenciaAdmin)