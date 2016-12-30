from django.conf.urls import *
from django.contrib import admin
from novedades.views import *

admin.autodiscover()

urlpatterns = patterns('',
	
    url(r'^admin/', include(admin.site.urls)),

    url(r'^index$', pagina_principal),
    url(r'^base$', base),
    url(r'^login$', login),
    url(r'^enviar', enviar),
    url(r'^formulario2/$', formulario2),
   

    url(r'^', include('novedades.urls')),

)