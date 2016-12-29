from django.conf.urls import *
from django.contrib import admin
from novedades.views import *
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^index$', pagina_principal),
    url(r'^base$', base),
    url(r'^login$', login),
    url(r'^formularioRegistro$', registro),
    url(r'^enviar', enviar),
    url(r'^formulario2/$', formulario2),

    url(r'^', include('novedades.urls')),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT,}),
)