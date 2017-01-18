from django.conf.urls import *
from django.contrib import admin
from usuarios.views import *

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^recuperar-contrasenia$', vista_recuperar_clave), 
	url(r'^registrarse$', vista_registrarse),
	url(r'^inicial-admin$', vista_inicial_admin),
	url(r'^modificar_perfil_alumno$', modificarPerfilAlumno),
	url(r'^cambiar-pass$', cambiar_contrasenia),
	url(r'^cambiar-telefono$', cambiar_telefono),
	url(r'^cambiar-direccion$', cambiar_direccion),

)
