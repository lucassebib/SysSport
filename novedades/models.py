from django.db import models
from tinymce import  models as tinymce_models
from django.contrib import admin

# Create your models here.

class Deporte(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField()

	class Meta:
		verbose_name_plural = "Deportes"

	def __unicode__(self):
		return self.nombre

class Persona(models.Model):
	legajo =  models.IntegerField()
	dni = models.IntegerField()
	nombre = models.CharField(max_length=100)
	apellido = models.CharField(max_length=100)
	fecha_nacimiento = models.DateField()
	telefono = models.IntegerField()
	email = models.EmailField()
	foto_perfil = models.ImageField(upload_to='fotos_de_perfil/')

class Profesor(Persona):
	lista_deporte = models.ManyToManyField(Deporte)

	class Meta:
		verbose_name_plural = "Profesores"

	def __unicode__(self):
		return '%s %s' % (self.nombre, self.apellido)

	def profesor_de(self):
		return "\n -".join([d.nombre for d in self.lista_deporte.all()])
		#return self.lista_deporte.all()

class Alumno(Persona):
	ficha_medica = models.FileField(upload_to='fichas_medicas/', blank=True)
	lista_deporte = models.ManyToManyField(Deporte)

	class Meta:
		verbose_name_plural = "Alumnos"

	def deportes_inscripto(self):
		return "\n -".join([d.nombre for d in self.lista_deporte.all()])

class ManejadorNovedades(models.Manager):
	def get_queryset(self):
		default_queryset = super(ManejadorNovedades, self).get_query_set()
		return default_queryset.filter(visibilidad__in=[1])

class Novedades(models.Model):
	pueden_ver = ((1,"Todos"),(2,"Todos los Usuarios Registrados"), (3, "Solo los Usuarios del Deporte"))

	titulo = models.CharField(max_length=100)
	contenido = tinymce_models.HTMLField()
	fecha_publicacion = models.DateField(blank=True, null=True)
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
	list_display = ('legajo','dni','nombre','apellido','fecha_nacimiento','telefono','email','profesor_de')

admin.site.register(Profesor,ProfesorAdmin)

class AlumnoAdmin(admin.ModelAdmin):
	list_display = ('legajo','dni', 'nombre', 'apellido','fecha_nacimiento','telefono','email', 'deportes_inscripto')
	filter_vertical = ('lista_deporte',)

admin.site.register(Alumno,AlumnoAdmin)

class NovedadesAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'visibilidad','autor')	

admin.site.register(Novedades,NovedadesAdmin)
