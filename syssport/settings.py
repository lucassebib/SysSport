# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.core.urlresolvers import reverse_lazy
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8h@d$dvno$6i-6!+(q9zih-1ttbm^w0#rxwpbca_^%h1s*ssu*'
 
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'novedades',
    'usuarios',
    'deportes',
    'canchas',
    'tinymce'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}

ROOT_URLCONF = 'syssport.urls'

WSGI_APPLICATION = 'syssport.wsgi.application'

TEMPLATE_DIRS = ('templates',)

TEMPLATE_CONTEXT_PROCESSORS = (
"django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages",
"django.core.context_processors.request",
)

#MEDIA_ROOT = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR,'media')

MEDIA_URL = '/media/'

STATICFILES_DIRS = ( 
    os.path.join(BASE_DIR,'media'),
    
)
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
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = reverse_lazy('url_login')

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

LOGIN_URL = reverse_lazy('url_login')

EMAIL_USE_TLS = True 
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'syssport2017@gmail.com'
EMAIL_HOST_PASSWORD ='proyecto2017'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'




