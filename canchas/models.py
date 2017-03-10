from django.contrib import admin
from django.db import models
from django.core.urlresolvers import reverse

from deportes.models import Deporte
from usuarios.models import Direccion


class Cancha(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField()	
	direccion = models.ForeignKey(Direccion, blank=True, null=True)

	def __unicode__(self):
		return self.nombre

	def get_absolute_url(self):
		return reverse('listar-canchas')

##################AGREGAMOS CLASES AL PANEL DE ADMINISTRACION##################################

class CanchaAdmin(admin.ModelAdmin):
	list_display = ('nombre',)

admin.site.register(Cancha,CanchaAdmin)
