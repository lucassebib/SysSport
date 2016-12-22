from django.conf.urls import *
from novedades.views import *

urlpatterns = patterns('',
	url(r'^inicial_alumnos$', inicial_alumnos),
)