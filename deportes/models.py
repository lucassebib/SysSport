from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse	

class Deporte(models.Model):
	generos_aptos = ((1,"Solo Masculino"), (2,"Solo Femenino"), (3,"Mixto")) 

	nombre = models.CharField(max_length=100)
	descripcion = models.TextField()
	apto_para = models.IntegerField(choices=generos_aptos, default=3)

	class Meta:
		verbose_name_plural = "Deportes"

	def __unicode__(self):
		return self.nombre

	def get_absolute_url(self):
		return reverse('listar-deportes')

##################AGREGAMOS CLASES AL PANEL DE ADMINISTRACION##################################

class DeporteAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'descripcion')

admin.site.register(Deporte,DeporteAdmin)