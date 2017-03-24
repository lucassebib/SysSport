from django.db import models

class Peticionesservidor(models.Model):
    peticion = models.IntegerField(db_column='PETICION', blank=True, null=True) # Field name made lowercase.
    idpetici_n = models.AutoField(db_column=u'IDPETICI\xd3N', primary_key=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    idexterna = models.CharField(db_column='IDEXTERNA', max_length=20, blank=True) # Field name made lowercase.
    estado = models.SmallIntegerField(db_column='ESTADO', blank=True, null=True) # Field name made lowercase.
    statussalida = models.TextField(db_column='STATUSSALIDA', blank=True) # Field name made lowercase.
    fecha = models.DateTimeField(db_column='FECHA', blank=True, null=True) # Field name made lowercase.
    parametro1 = models.TextField(db_column='PARAMETRO1', blank=True) # Field name made lowercase.
    parametro2 = models.TextField(db_column='PARAMETRO2', blank=True) # Field name made lowercase.
    parametro3 = models.TextField(db_column='PARAMETRO3', blank=True) # Field name made lowercase.
    instancia = models.CharField(db_column='INSTANCIA', max_length=20, blank=True) # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'PeticionesServidor'
