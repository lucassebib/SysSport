from django.conf.urls import *
from django.contrib import admin
from usuarios.views import *

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^recuperar-contrasenia$', vista_recuperar_clave), 
	url(r'^registrarse$', vista_registrarse),
	url(r'^inicial-admin$', vista_inicial_admin),
	url(r'^modificar_perfil_alumno$', modificarPerfilAlumno, name='modificar_perfil_alumno'),
	url(r'^cambiar-pass$', cambiar_contrasenia),
	url(r'^cambiar-telefono$', cambiar_telefono),
	url(r'^cambiar-direccion$', cambiar_direccion),
	url(r'^ver-deportes$', ver_deportes_profesor, name='ver-deportes'),
	url(r'^ver-alumnos/deporte/(?P<pk>[0-9]+)$', listar_alumnos_deporte, name='ver-alumnos'),

)
