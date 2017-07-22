from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Entrenamiento(models.Model):
	lista_dias = ((1, "Lunes"), (2, "Martes"), (3, "Miercoles"), (4, "Jueves"), (5, "Viernes"), (6, "Sabado"), (7, "Domingo")) 
	
	dia = models.IntegerField(choices=lista_dias, default=1)
	
	hora_inicio = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                       MaxValueValidator(24)], blank=True, null=True)
	minutos_inicio = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                       MaxValueValidator(59)], blank=True, null=True)
	hora_fin = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                       MaxValueValidator(24)], blank=True, null=True)
	minutos_fin = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                       MaxValueValidator(59)], blank=True, null=True)
	
	def ver_dia(self):
		return self.get_dia_display()

	def ver_horario_inicio(self):
		return   ('0' if self.hora_inicio < 10 else '') +  str(self.hora_inicio) + ':' + ('0' if self.minutos_inicio < 10 else '') +  str(self.minutos_inicio)

	def ver_horario_fin(self):
		return   ('0' if self.hora_fin < 10 else '') +  str(self.hora_fin) + ':' + ('0' if self.minutos_fin < 10 else '') +  str(self.minutos_fin)
		
		



