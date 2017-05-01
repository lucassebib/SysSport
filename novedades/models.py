from django.contrib.auth.models import User
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.html import strip_tags
from tinymce import  models as tinymce_models

from usuarios.models import Profesor
from deportes.models import Deporte
from usuarios.models import Persona, Alumno


class Comentario(models.Model):
	texto = models.TextField( verbose_name ='comentario')
	autor = models.IntegerField()
	nombre_autor = models.CharField(max_length=150, blank=True, null=True)

	def obtener_url_imagen(self):
		id_autor = self.autor
		try:
			url_foto = Persona.objects.get(id=id_autor).foto_perfil.url
		except Exception as e:
			url_foto = Alumno.objects.get(id=id_autor).foto_perfil.url
		
		return url_foto
		
	def obtener_idAutor(self):
		return self.autor

	def es_admin(self):
		a=False
		try:
			a = User.objects.get(id=self.autor).is_staff
		except Exception as e:
			print(e)
		print(a)
		return a

LIMITE_CARACTERES_NOVEDAD = 250
class Novedades(models.Model):
	pueden_ver = ((1,"Todas las personas"),(2,"Todos los Usuarios Registrados"), (3, "Solo los Usuarios del Deporte"))
	titulo = models.CharField(max_length=100)
	contenido = tinymce_models.HTMLField()
	fecha_publicacion = models.DateTimeField(auto_now_add=True)
	#autor = models.ForeignKey(Profesor, blank=True, null=True)
	autor = models.ForeignKey(User, blank=True, null=True)   
	imagen = models.ImageField(upload_to='fotos_posts', blank=True, null=True)
	visibilidad = models.IntegerField(choices=pueden_ver, default=2)
	categoria = models.ManyToManyField(Deporte, blank=True, null=True)
	lista_comentarios = models.ManyToManyField(Comentario, blank=True, null=True)

	class Meta:
		verbose_name_plural = "Novedades" 

	def obtener_categorias(self):
		return "\n -".join([d.nombre for d in self.categoria.all()])

	#def obtener_textoComentarios(self):
	#	return "\n -".join([t.texto for t in self.lista_comentarios.all()])
	
	#def obtener_autoresComentario(self):
	#	return "\n -".join([d.autor for d in self.lista_comentarios.all()])

	def get_absolute_url(self):
		return reverse('listar-novedades')

	def obtener_url_imagen(self):
		id_autor = self.autor.id
		url_foto = Persona.objects.get(id=id_autor).foto_perfil.url
		return url_foto

	def obtener_idAutor(self):
		a = self.autor
		return self.autor.id

	def ver_visibilidad(self):
		return self.get_visibilidad_display()

	def es_admin(self):
		a=False
		try:
			a = User.objects.get(id=self.autor.id).is_staff
		except Exception as e:
			print(e)
		print(a)
		return a

	def reducir_texto(self):
		return strip_tags(self.contenido)[:LIMITE_CARACTERES_NOVEDAD]

class Notificacion(models.Model):
	id_autor_comentario = models.IntegerField()
	autor_comentario = models.CharField(max_length=50)
	notificar_a = models.ForeignKey(User)
	novedad = models.ForeignKey(Novedades)


##################AGREGAMOS CLASES AL PANEL DE ADMINISTRACION##################################

class NovedadesAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'fecha_publicacion' ,'visibilidad','autor', 'obtener_categorias')	

admin.site.register(Novedades,NovedadesAdmin)



