import xml.etree.ElementTree as ET
import time

from datetime import datetime

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
	