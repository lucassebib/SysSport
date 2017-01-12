from django.conf.urls import *
from django.contrib import admin
from usuarios.views import *

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^recuperar-contrasenia$', vista_recuperar_clave), 
	url(r'^registrarse$', vista_registrarse),

)
