from django.db import models
from tinymce import  models as tinymce_models
from django.contrib import admin
from usuarios.models import Profesor
from deportes.models import Deporte
from django.core.urlresolvers import reverse

class Novedades(models.Model):
	pueden_ver = ((1,"Todos"),(2,"Todos los Usuarios Registrados"), (3, "Solo los Usuarios del Deporte"))

	titulo = models.CharField(max_length=100)
	contenido = tinymce_models.HTMLField()
	fecha_publicacion = models.DateTimeField(auto_now_add=True)
	autor = models.ForeignKey(Profesor)   
	imagen = models.ImageField(upload_to='fotos_posts', blank=True, null=True)
	visibilidad = models.IntegerField(choices=pueden_ver, default=3)
	categoria = models.ManyToManyField(Deporte)

	class Meta:
		verbose_name_plural = "Novedades" 

	def obtener_categorias(self):
		return "\n -".join([d.nombre for d in self.categoria.all()])


	#def __unicode__(self):
	#	return self.nombre

	def get_absolute_url(self):
		return reverse('detalle-novedad',kwargs={'pk': self.pk})

##################AGREGAMOS CLASES AL PANEL DE ADMINISTRACION##################################

class NovedadesAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'fecha_publicacion' ,'visibilidad','autor', 'obtener_categorias')	

admin.site.register(Novedades,NovedadesAdmin)



