from django.conf.urls import *
from django.contrib import admin
from views import *

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^deportes/$', ListarDeportes.as_view(), name='listar-deporte'),
    url(r'^deportes/(?P<pk>[0-9]+)/$', DetallesDeportes.as_view(), name='deporte-detalles'),
    url(r'^deportes/crear/$', CrearDeportes.as_view(), name='crear-deporte'),
    url(r'^deportes/(?P<pk>[0-9]+)/modificar/$', ActualizarDeportes.as_view(), name='deporte-actualizar'),
    url(r'^deportes/(?P<pk>[0-9]+)/eliminar/$', EliminarDeportes.as_view(), name='eliminar-deportes'),
)
