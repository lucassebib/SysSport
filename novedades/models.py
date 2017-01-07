from django.db import models
from tinymce import  models as tinymce_models
from django.contrib import admin
from django.contrib.auth.models import User as Usuario

# Create your models here.

class Deporte(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField()

	class Meta:
		verbose_name_plural = "Deportes"

	def __unicode__(self):
		return self.nombre

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
	legajo =  models.IntegerField()
	ficha_medica = models.FileField(upload_to='fichas_medicas/', blank=True)
	

	class Meta:
		verbose_name_plural = "Alumnos"

	def deportes_inscripto(self):
		return "\n -".join([d.nombre for d in self.lista_deporte.all()])

	def tipo_usuario(self, cadena):
		return cadena == 'alumno'

class UsuarioInvitado(Persona): 
	institucion = models.CharField(max_length=100)
	ficha_medica = models.FileField(upload_to='fichas_medicas/', blank=True)

	class Meta:
		verbose_name_plural = "UsuariosInvitados"

	def deportes_inscripto(self):
		return "\n -".join([d.nombre for d in self.lista_deporte.all()])

	def tipo_usuario(self, cadena):
		return cadena=='invitado'

class ManejadorNovedades(models.Manager):
	def get_queryset(self):
		default_queryset = super(ManejadorNovedades, self).get_query_set()
		return default_queryset.filter(visibilidad__in=[1])

class Novedades(models.Model):
	pueden_ver = ((1,"Todos"),(2,"Todos los Usuarios Registrados"), (3, "Solo los Usuarios del Deporte"))

	titulo = models.CharField(max_length=100)
	contenido = tinymce_models.HTMLField()
	fecha_publicacion = models.DateTimeField(auto_now_add=True)
	autor = models.ForeignKey(Profesor)  
	imagen = models.ImageField(upload_to='fotos_posts', blank=True, null=True)
	visibilidad = models.IntegerField(choices=pueden_ver, default=3)

	objects = models.Manager()
	todos_novedades_objects = ManejadorNovedades()

	class Meta:
		verbose_name_plural = "Novedades" 

##################AGREGAMOS CLASES AL PANEL DE ADMINISTRACION##################################

class DeporteAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'descripcion')

admin.site.register(Deporte,DeporteAdmin)

class ProfesorAdmin(admin.ModelAdmin):
	list_display = ('legajo','dni','fecha_nacimiento','telefono','email','profesor_de')
	fields = ('username', 'password', 'first_name', 'last_name', 'legajo', 'dni', 'fecha_nacimiento', 'telefono', 'foto_perfil', 'lista_deporte', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')


admin.site.register(Profesor,ProfesorAdmin)

class AlumnoAdmin(admin.ModelAdmin):
	list_display = ('legajo', 'deportes_inscripto')
	fields = ('username', 'password', 'first_name', 'last_name', 'legajo', 'dni', 'fecha_nacimiento', 'telefono', 'foto_perfil', 'lista_deporte', 'ficha_medica', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')

admin.site.register(Alumno,AlumnoAdmin)

class UsuarioInvitadoAdmin(admin.ModelAdmin):
	list_display = ('institucion', 'deportes_inscripto')
	fields = ('username', 'password', 'first_name', 'last_name', 'dni', 'institucion' , 'fecha_nacimiento', 'telefono', 'foto_perfil', 'lista_deporte', 'ficha_medica', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')

admin.site.register(UsuarioInvitado,UsuarioInvitadoAdmin)


class NovedadesAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'fecha_publicacion' ,'visibilidad','autor')	

admin.site.register(Novedades,NovedadesAdmin)
