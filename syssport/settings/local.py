from .base import *

DEBUG = True
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'sqlserver_ado',
        'NAME': 'syssport',
        'HOST': 'localhost',

        'USER': 'proyecto',
        'PASSWORD': 'proyecto2016',

        'OPTIONS': {
                    'uncicode_result': 'True',
                    'provider': 'SQLNCLI11',
                    'use_mars': 'DataTypeCompatibility=80;MARS Connection=True;'
        }
    },

    'sysacad': {
        'ENGINE': 'sqlserver_ado',
        'NAME': 'SYSACAD',
        'HOST': '10.13.0.112',
        'USER': 'usrsysacadweb',
        'PASSWORD': 'deportes123',      
    }

}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
