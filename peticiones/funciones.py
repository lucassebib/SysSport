import xml.etree.ElementTree as ET
import time

from datetime import datetime, date



from peticiones.models import Peticionesservidor


def establecer_conexion(username, password):
	permitecursado = ''
	fecha = datetime.now().strftime('%Y%m%d%H%M%S')
	IDEXTERNA = str(fecha) + str(username) + 'D'
	peticion = Peticionesservidor()
	peticion.peticion = 300
	peticion.idexterna = IDEXTERNA
	peticion.estado = 0
	peticion.parametro1 = '<?xml version = "1.0" encoding="Windows-1252" standalone="yes"?> <VFPData> <_parametro1> <legajo>'+str(username)+'</legajo> <dni>00</dni> <password>"'+password+'"</password> <tipologueo>3</tipologueo> </_parametro1> </VFPData>'
	try:
		peticion.save(force_insert = True, using='sysacad')
		for x in range(20):
			time.sleep(0.5)
			newPeticion = Peticionesservidor.objects.using('sysacad').get(idexterna = IDEXTERNA)
			if newPeticion.estado > 1:
				break
	except Exception as a:
		return a
	return newPeticion

def autenticacion(username, password):
	estado = establecer_conexion(username, password).estado
	if estado == 3:
		#todo mal
		return False
	else:
		if estado == 2:
			return True

def obtener_datos_iniciales(username, password):
	peticion = establecer_conexion(username, password)
	paramXML = ET.fromstring(peticion.parametro2.encode('ISO-8859-1'))
	print(peticion.parametro2)
	diccionario = {}
	for x in paramXML:
		for z in x:
			if z.tag == 'nombre':
				nombre_completo = z.text
				corte = nombre_completo.split(", ")
				nombre = corte[1]
				apellido = corte[0]
				temp = {'nombre': nombre, 'apellido': apellido}
				diccionario.update(temp)
			elif z.tag == 'codespecialidad':
				temp = {'carrera': int(z.text)}
				diccionario.update(temp)

	return diccionario

def add_months(sourcedate,months):
	month = sourcedate.month - 1 + months
	year = sourcedate.year + month / 12
	month = month % 12 + 1
	day = min(sourcedate.day,calendar.monthrange(year,month)[1])
	return datetime.date(year,month,day)

def obtener_datos_academicos(username, f_desde, f_hasta):
	year,month,day = f_desde.split('-')
	desde = date(int(year),int(month),int(day))
	
	string(desde)
	""" 
		Devuelve la cantidad de materias aprobobadas por un alumno en el rango de fechas que se reciben por parametro
	"""

	notas = {
		'cuatro': 4,
		'cinco': 5,
		'seis': 6,
		'siete': 7,
		'ocho': 8,
		'nueve': 9,
		'diez': 10,
	}

	legajo = username 
	fecha = datetime.now().strftime('%Y%m%d%H%M%S')
	IDEXTERNA = str(fecha) + str(username) + 'D'
	peticion = Peticionesservidor()
	peticion.peticion = 206
	peticion.idexterna = IDEXTERNA
	peticion.estado = 0
	peticion.parametro1 = '<?xml version = "1.0" encoding="Windows-1252" standalone="yes"?><VFPData><parametro1><legajo>'+legajo+'</legajo></parametro1> </VFPData>'
	cont = 0

	try:
		peticion.save(force_insert = True, using='sysacad')
		for x in range(20):
			time.sleep(0.5)
			newPeticion = Peticionesservidor.objects.using('sysacad').get(idexterna = IDEXTERNA)
			if newPeticion.estado > 1:
				break
	except Exception as a:
		return a

	paramXML = ET.fromstring(newPeticion.parametro2.encode('ISO-8859-1'))

	for x in paramXML:
		for z in x:
			if z.tag == 'fecha':
				c = 1
			
			if z.tag == 'nota':
				calificacion = notas.get(nota)
				if calificacion>=4:
					cont = cont + 1

	return cont



		
		
	