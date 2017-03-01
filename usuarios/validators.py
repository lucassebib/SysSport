from django.core.exceptions import ValidationError
	 
def valid_extension(value):
	#Esta funcion valida extension .pdf .doc y .docx
	#Afecta a otros modelos, no cambiar las extensiones que valida

    if (not value.name.endswith('.pdf') and
        not value.name.endswith('.doc') and 
        not value.name.endswith('.docx')):
 
        raise ValidationError("Archivos permitidos: .pdf, .doc, .docx")


