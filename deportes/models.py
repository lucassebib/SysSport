from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse	

class Deporte(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField()

	class Meta:
		verbose_name_plural = "Deportes"

	def __unicode__(self):
		return self.nombre

	def get_absolute_url(self):
		return reverse('deporte-detalles',kwargs={'pk': self.pk})

##################AGREGAMOS CLASES AL PANEL DE ADMINISTRACION##################################

class DeporteAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'descripcion')

admin.site.register(Deporte,DeporteAdmin)