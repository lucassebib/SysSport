from django.conf.urls import *
from novedades.views import *
from django.contrib.auth.views import login 

urlpatterns = patterns('',
	url(r'^inicial_alumnos$', vista_index_alumnos),
    url(r'^inicial_profesores$', vista_index_profesores),
    url(r'^inicial_invitados$', vista_index_invitados), 	
)