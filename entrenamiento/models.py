from django.contrib import admin
from django.db import models

class Entrenamiento(models.Model):
	lista_dias = ((1, "Lunes"), (2, "Martes"), (3, "Miercoles"), (4, "Jueves"), (5, "Viernes"), (6, "Sabado"), (7, "Domingo")) 
	lista_horarios = ((1, "07:00"), (2, "07:30"), (3, "08:00"), (4, "08:30"), (5, "09:00"), (6, "09:30"), 
				      (7, "10:00"), (8, "10:30"), (9, "11:00"), (10, "11:30"), (11, "12:00"), (12, "12:30"),
				      (13, "13:00"), (14, "13:30"), (15, "14:00"), (16, "14:30"), (17, "15:00"), (18, "15:30"),
				      (20, "16:00"), (21, "16:30"), (22, "17:00"), (23, "17:30"), (24, "18:00"), (25, "18:30"),
				      (26, "19:00"), (27, "19:30"), (28, "20:00"), (29, "20:30"), (30, "21:00"), (31, "21:30"),
				      (32, "22:00"), (33, "22:30"), (34, "23:00"), (35, "23:30"), (36, "00:00"), (37, "00:30"))
	
	dia = models.IntegerField(choices=lista_dias, default=1)
	horario_inicio = models.IntegerField(choices=lista_horarios, verbose_name='Hora de Inicio', default=1) 
	horario_fin = models.IntegerField(choices=lista_horarios, verbose_name='Hora de Finalizacion', default=2)

	def ver_dia(self):
		return self.get_dia_display()

	def ver_horario_inicio(self):
		return self.get_horario_inicio_display()

	def ver_horario_fin(self):
		return self.get_horario_fin_display()

	def ver_horario_completo(self):
		return self.get_dia_display() + ' de ' + self.get_horario_inicio_display() + ' hs. ' + 'a ' + self.get_horario_fin_display() + ' hs.'


		
		



