from django.conf.urls import *
from django.contrib import admin
from views import *

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^canchas/$', ListarCanchas.as_view(), name='listar-canchas'),
    url(r'^canchas/(?P<pk>[0-9]+)/$', DetallesCanchas.as_view(), name='cancha-detalles'),
    url(r'^canchas/crear/$', CrearCanchas.as_view(), name='crear-cancha'),
    url(r'^canchas/(?P<pk>[0-9]+)/modificar/$', ActualizarCanchas.as_view(), name='cancha-actualizar'),
    url(r'^canchas/(?P<pk>[0-9]+)/eliminar/$', EliminarCanchas.as_view(), name='eliminar-canchas'),
)
