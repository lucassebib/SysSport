from django.db import models
from tinymce import  models as tinymce_models
from django.contrib import admin
from usuarios.models import Profesor
from deportes.models import Deporte
from usuarios.models import Persona
from django.core.urlresolvers import reverse

class Comentario(models.Model):
	texto = models.TextField( verbose_name ='comentario')
	autor = models.ForeignKey(Persona)

	def obtener_url_imagen(self):
		id_autor = self.autor.id
		url_foto = Persona.objects.get(id=id_autor).foto_perfil.url
		return url_foto
		
	def obtener_idAutor(self):
		return self.autor.id

class Novedades(models.Model):
	pueden_ver = ((1,"Todas las personas"),(2,"Todos los Usuarios Registrados"), (3, "Solo los Usuarios del Deporte"))

	titulo = models.CharField(max_length=100)
	contenido = tinymce_models.HTMLField()
	fecha_publicacion = models.DateTimeField(auto_now_add=True)
	autor = models.ForeignKey(Profesor)   
	imagen = models.ImageField(upload_to='fotos_posts', blank=True, null=True)
	visibilidad = models.IntegerField(choices=pueden_ver, default=2)
	categoria = models.ManyToManyField(Deporte)
	lista_comentarios = models.ManyToManyField(Comentario, blank=True, null=True)

	class Meta:
		verbose_name_plural = "Novedades" 

	def obtener_categorias(self):
		return "\n -".join([d.nombre for d in self.categoria.all()])

	def obtener_textoComentarios(self):
		return "\n -".join([t.texto for t in self.lista_comentarios.all()])
	
	#def obtener_autoresComentario(self):
	#	return "\n -".join([d.autor for d in self.lista_comentarios.all()])

	def get_absolute_url(self):
		return reverse('listar-novedades')

	def obtener_url_imagen(self):
		id_autor = self.autor.id
		url_foto = Persona.objects.get(id=id_autor).foto_perfil.url
		return url_foto

	def obtener_idAutor(self):
		return self.autor.id

##################AGREGAMOS CLASES AL PANEL DE ADMINISTRACION##################################

class NovedadesAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'fecha_publicacion' ,'visibilidad','autor', 'obtener_categorias')	

admin.site.register(Novedades,NovedadesAdmin)



