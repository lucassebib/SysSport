from django.core.paginator import Paginator

def Paginate(request, queryset, pages):
    """
    PARAMETROS:
    request: Request de la vista
    queryset: Queryset a utilizar en la paginacion
    pages: Cantidad de paginas del paginador
    """
    # Retorna el objeto paginator para comenzar el trabajo
    result_list = Paginator(queryset, pages)
 
    try:
        # Tomamos el valor de parametro page, usando GET
        page = int(request.GET.get('page'))
    except:
        page = 1
 
    # Si es menor o igual a 0 igualo en 1
    if page <= 0:
        page = 1
 
    # Si viene un parametro que es mayor a la cantidad
    # de paginas le igualo el parametro con las cant de paginas
    if(page > result_list.num_pages):
        page = result_list.num_pages
 
    # Verificamos si esta dentro del rango
    if (result_list.num_pages >= page):
        # Obtengo el listado correspondiente al page
        pagina = result_list.page(page)
 
        context = {
            'queryset': pagina.object_list,
            'page': page,
            'pages': result_list.num_pages,
            'list_page': range(1, result_list.num_pages + 1),
            'has_next': pagina.has_next(),
            'has_prev': pagina.has_previous(),
            'next_page': page+1,
            'prev_page': page-1,
            'firstPage': 1,
        }
 
    return context