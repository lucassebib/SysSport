from django.db import models

from django.contrib import admin

# Create your models here.

class Deporte(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField()

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

	def __unicode__(self):
		return '%s %s' % (self.nombre, self.apellido)

	def profesor_de(self):
		return "\n -".join([d.nombre for d in self.lista_deporte.all()])
		#return self.lista_deporte.all()

class Alumno(Persona):
	ficha_medica = models.FileField(upload_to='fichas_medicas/')
	lista_deporte = models.ManyToManyField(Deporte)

	def deportes_inscripto(self):
		return "\n -".join([d.nombre for d in self.lista_deporte.all()])

class Novedades(models.Model):
	titulo = models.CharField(max_length=100)
	contenido = models.TextField()
	fecha_publicacion = models.DateField()
	autor = models.ForeignKey(Profesor)  
	pueden_ver = ((1,"Todos"),(2,"Usuarios Deportes")) 

##################AGREGAMOS CLASES AL PANEL DE ADMINISTRACION##################################

class DeporteAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'descripcion')

admin.site.register(Deporte,DeporteAdmin)

class ProfesorAdmin(admin.ModelAdmin):
	list_display = ('legajo','dni','nombre','apellido','fecha_nacimiento','telefono','email','profesor_de')

admin.site.register(Profesor,ProfesorAdmin)

class AlumnoAdmin(admin.ModelAdmin):
	list_display = ('legajo','dni', 'nombre', 'apellido','fecha_nacimiento','telefono','email', 'deportes_inscripto')

admin.site.register(Alumno,AlumnoAdmin)

class NovedadesAdmin(admin.ModelAdmin):
	list_display = ('titulo','contenido','fecha_publicacion')

admin.site.register(Novedades,NovedadesAdmin)
