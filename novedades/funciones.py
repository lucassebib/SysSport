#-!-coding: utf-8 -!-
import datetime
from datetime import date
from novedades.models import *
	# BUSCADOR
def buscador_novedades(request, consulta, mensaje):	
	query = request.GET.get('q', '')
	if request.method == 'GET' and 'btn_buscar' in request.GET:
		if query:
			if not request.GET.get('opcion'):
				mensaje = 'No ha introducido ningún parámetro de búsqueda.'
				consulta=''
			else:
				#     BUSQUEDA POR TITULO
				if request.GET.get('opcion') == 'titulo':
					titulo = request.GET.get('q')
					consulta = consulta.filter(titulo__icontains=titulo)
					if not consulta:
						mensaje = 'No se han encontrado coincidencias'

				else:
					#   BUSQUEDA POR FECHA
					if request.GET.get('opcion')=='fecha':
						fecha = request.GET.get('q')
						seleccionados = request.POST.getlist("fecha")						

						#VALIDAR ENTRADA DE FECHA
						valido = False
						if 'dia' in seleccionados and 'mes' in seleccionados and 'anio' in seleccionados:
							#DD/MM/YYYY
							dia = fecha[:2]
							separador1 = fecha[2]
							mes = fecha[3:5]
							separador2 = fecha[5]
							anio = fecha[6:]
							cadena = dia+mes+anio
							if cadena.isdigit() and separador1==separador2 and (separador1=='/' or separador1=='-') and len(fecha) == 10:
								valido = True								
						else:
							if 'dia' in seleccionados and 'mes' in seleccionados and not 'anio' in seleccionados:
								#DD/MM
								dia = fecha[:2]
								separador1 = fecha[2]
								mes = fecha[3:5]
								cadena = dia + mes 
								if cadena.isdigit() and (separador1=='/' or separador1=='-') and len(fecha) == 5:
									valido = True

							else:
								if 'dia' in seleccionados and 'anio' in seleccionados and not 'mes' in seleccionados:
									#DD/YYYY
									dia = fecha[:2]
									separador1 = fecha[2]
									anio = fecha[3:8]
									cadena = dia+anio
									if cadena.isdigit() and (separador1=='/' or separador1=='-') and len(fecha) == 7:
										valido = True
								else:
									if 'mes' in seleccionados and 'anio' in seleccionados and not 'dia' in seleccionados:
										#MM/YYYY
										mes = fecha[:2]
										separador1 = fecha[2]
										anio = fecha[3:8]
										cadena = mes+anio
										if cadena.isdigit() and (separador1=='/' or separador1=='-') and len(fecha) == 7:
											valido = True
									else:
										if 'anio' in seleccionados and not 'dia' in seleccionados and not 'mes' in seleccionados:
											#YYYY
											anio = fecha[:4]
											if anio.isdigit() and len(anio) == 4:
												valido = True	
										else:
											if 'dia' in seleccionados and not 'anio' in seleccionados and not 'mes' in seleccionados:
												#DD
												dia = fecha[:2]
												if dia.isdigit() and len(dia) == 2:
													valido = True
											else:
												if mes and not anio and not dia:
													#MM
													mes = fecha[:2]
													if mes.isdigit() and len(mes) == 2:
														valido = True
													
						if valido:
							#ENTRADA CORRECTA
							#SE REALIZA LA BUSQUEDA POR FECHA
							if 'dia' in seleccionados and 'mes' in seleccionados and 'anio' in seleccionados:
								#DD/MM/YYYY
								dia = fecha[:2]
								mes = fecha[3:5]
								anio = fecha[6:]
								fecha2 = datetime.date(int(anio), int(mes), int(dia))
								consulta = consulta.filter(fecha_publicacion__icontains=fecha2)
							else:
								if 'dia' in seleccionados and 'mes' in seleccionados and not 'anio' in seleccionados:
									#DD/MM
									dia = fecha[:2]
									mes = fecha[3:5]
									fecha2 = datetime.date(1, int(mes), int(dia))
									consulta = consulta.filter(fecha_publicacion__day = fecha2.day, fecha_publicacion__month = fecha2.month)
								else:
									if 'dia' in seleccionados and 'anio' in seleccionados and not 'mes' in seleccionados:
										#DD/YYYY
										dia = fecha[:2]
										anio = fecha[3:8]
										fecha2 = datetime.date(int(anio), 1, int(dia))
										consulta = consulta.filter(fecha_publicacion__day = fecha2.day, fecha_publicacion__year = fecha2.year)
									else:
										if 'mes' in seleccionados and 'anio' in seleccionados and not 'dia' in seleccionados:
											#MM/YYYY
											mes = fecha[:2]
											anio = fecha[3:8]
											fecha2 = datetime.date(int(anio), int(mes), 1)
											consulta = consulta.filter(fecha_publicacion__month = fecha2.month, fecha_publicacion__year = fecha2.year)
										else:
											if 'anio' in seleccionados and not 'dia' in seleccionados and not 'mes' in seleccionados:
												#YYYY
												anio = fecha[:4]
												fecha2 = datetime.date(int(anio), 1, 1)
												consulta = consulta.filter(fecha_publicacion__year = fecha2.year)
											else:
												if 'dia' in seleccionados and not 'anio' in seleccionados and not 'mes' in seleccionados:
													#DD
													dia = fecha[:2]
													fecha2 = datetime.date(1, 1, int(dia))
													consulta = consulta.filter(fecha_publicacion__day = fecha2.day)
												else:
													if mes and not anio and not dia:
														#MM
														mes = fecha[:2]
														fecha2 = datetime.date(1, int(mes), 1)
														consulta = consulta.filter(fecha_publicacion__month = fecha2.month)

							if not consulta:
								mensaje = 'No se han encontrado coincidencias'
						else:
							consulta = ''
							mensaje = 'Por favor, introduzca una fecha con el formato DD/MM/YYYY o DD-MM-YYYY, de acuerdo a su opcion de busqueda'
					
					else:
						# BUSQUEDA POR AUTOR
						if request.GET.get('opcion')=='autor':
							nombre_apellido = request.GET.get('q')
							if 'opcion_autor' in request.GET:
								if request.GET.get('opcion_autor')=='nombre':
									usuarios = User.objects.filter(first_name__icontains=nombre_apellido)
								else:
									usuarios = User.objects.filter(last_name__icontains=nombre_apellido)
							else:
								consulta = ''
								mensaje = 'No ha ingresado ningun parámetro de búsqueda para Autor.'
							
							consulta = consulta.filter(autor__in = usuarios)
							if not consulta:
								consulta = ''
								mensaje = 'No se han encontrado coincidencias para: ' +  request.GET.get('q')
	
	return consulta, mensaje, query
	#finBUSCADOR
	
	#BUSCADOR_POR_TITULO
	def buscador_novedades_por_titulo(request, consulta, mensaje):	

		if request.method == 'GET' and 'btn_buscar' in request.GET:
			if request.GET.get('q', '')=='':
				mensaje = 'No ha introducido ningun termino en la busqueda'
				consulta= ''
			else:
				if not request.GET.get('opcion'):
					mensaje = 'No ha introducido ningun parametro de busqueda'
					consulta=''
				else:
					#     BUSQUEDA POR TITULO
					if request.GET.get('opcion') == 'titulo':
						titulo = request.GET.get('q')
						consulta = consulta.filter(titulo__icontains=titulo)
						if not consulta:
							mensaje = 'No se han encontrado coincidencias'

	return consulta, mensaje, query
	#finBUSCADOR

#*************************************************************************************
