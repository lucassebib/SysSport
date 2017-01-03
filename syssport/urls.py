from django.conf.urls import *
from django.contrib import admin
from novedades.views import *

admin.autodiscover()

urlpatterns = patterns('',
	
    url(r'^admin/', include(admin.site.urls)),

    url(r'^index$', pagina_principal),
    url(r'^base$', base),
    url(r'^login2$', login),
    url(r'^formularioRegistro$', registro),
    url(r'^enviar', enviar),
    url(r'^formulario2/$', formulario2),

    url(r'^', include('novedades.urls')),

    url(r'^hola$', app_home, name="url_home"),
    url(r'^autenticar/$', app_login, name="url_login"),
    url(r'^logout/$', app_logout, name="url_logout"),

)