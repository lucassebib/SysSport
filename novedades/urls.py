from django.conf.urls import *
from novedades.views import *
from django.contrib.auth.views import login 

urlpatterns = patterns('',
	url(r'^inicial_alumnos$', inicial_alumnos),
	
)