#-!-coding: utf-8 -!-
from django.db.models import Q
from deportes.models import Deporte

# BUSCADOR
def buscador_deportes(request, consulta, mensaje):  
    query = request.GET.get('q', '')
    if query:
        if not request.GET.get('opcion'):
            mensaje = 'No ha introducido ningún parámetro de búsqueda.'
            consulta=''
        else:
            #     BUSQUEDA POR TITULO
            if request.GET.get('opcion') == 'nombre':
                qset = (
                    Q(nombre__icontains=query)
                )
                consulta = consulta.filter(qset)
                if not consulta:
                    mensaje = 'No se han encontrado coincidencias.'
       
    return consulta, mensaje, query
#finBUSCADOR

    