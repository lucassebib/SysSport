from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse
from usuarios.validators import valid_extension	
import os 

def generar_rutaID(instance, filename):
#	extension = os.path.splitext(filename)[1]
#	id_fm = super(generar_rutaID)
#	filename = "fm_" + str(instance.nombre) + str(extension)
	return ""	

class FichaMedica(models.Model):
	ficha_medica = models.FileField(upload_to='usuarios/deportes/fichas_medicas/', blank=True, validators=[valid_extension])
	descripcion = models.TextField()

	def obtenerNombreArchivo(self):
		return os.path.basename(self.ficha_medica.name)
	
class Deporte(models.Model):
	generos_aptos = ((1,"Solo Masculino"), (2,"Solo Femenino"), (3,"Mixto")) 

	nombre = models.CharField(max_length=100)
	descripcion = models.TextField()
	apto_para = models.IntegerField(choices=generos_aptos, default=3)
	ficha_medica = models.ForeignKey(FichaMedica, null=True, blank=True)

	class Meta:
		verbose_name_plural = "Deportes"

	def __unicode__(self):
		return self.nombre

	def get_absolute_url(self):
		return reverse('listar-deportes')
	
	def ver_aptopara(self):
		return self.get_apto_para_display()

##################AGREGAMOS CLASES AL PANEL DE ADMINISTRACION##################################
class FichaMedicaAdmin(admin.ModelAdmin):
	list_display = ['descripcion']

admin.site.register(FichaMedica, FichaMedicaAdmin)

class DeporteAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'descripcion', 'apto_para')

admin.site.register(Deporte,DeporteAdmin)

