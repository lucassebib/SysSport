from django.conf.urls import *
from django.contrib import admin
from views import *

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^deportes/$', lista_deportes, name='lista_deportes'),
    url(r'^deportes/(?P<pk>[0-9]+)/$', DetallesDeportes.as_view(), name='deporte-detalles'),
    url(r'^deportes/crear/$', CrearDeportes.as_view(), name='crear-deporte'),
    url(r'^deportes/(?P<pk>[0-9]+)/modificar/$', ActualizarDeportes.as_view(), name='deporte-actualizar'),
    url(r'^deportes/(?P<pk>[0-9]+)/eliminar/$', EliminarDeportes.as_view(), name='eliminar-deportes'),

    url(r'^ver-lista-deportes$',ver_deportes_personas, name='ver_deportes_personas'),
    url(r'^listar_deportes$',listar_deportes, name='listar_deportes'),
    url(r'^inscripcion_deportes$',inscripcion_deportes, name='inscribir_deportes'),
    url(r'^baja_deporte/(?P<pk>[0-9]+)$',baja_deporte, name='desinscribir_deporte'),
    url(r'^inscribir_deporte/(?P<pk>[0-9]+)$',inscribir_deporte, name='inscripcion_deporte'),
)
