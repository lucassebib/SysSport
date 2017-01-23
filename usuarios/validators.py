from django.core.exceptions import ValidationError
 
def valid_extension(value):
    if (not value.name.endswith('.pdf') and
        not value.name.endswith('.doc') and 
        not value.name.endswith('.docx')):
 
        raise ValidationError("Archivos permitidos: .pdf, .doc, .docx")


