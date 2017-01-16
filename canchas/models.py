from django.db import models
from django.contrib import admin
from deportes.models import Deporte
from usuarios.models import Direccion
from django.core.urlresolvers import reverse

class Cancha(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField()	
	deportes_aptos = models.ManyToManyField(Deporte)
	direccion = models.ForeignKey(Direccion, blank=True, null=True)

	def __unicode__(self):
		return self.nombre

	def get_absolute_url(self):
		return reverse('cancha-detalles',kwargs={'pk': self.pk})

##################AGREGAMOS CLASES AL PANEL DE ADMINISTRACION##################################

class CanchaAdmin(admin.ModelAdmin):
	list_display = ('nombre',)

admin.site.register(Cancha,CanchaAdmin)
