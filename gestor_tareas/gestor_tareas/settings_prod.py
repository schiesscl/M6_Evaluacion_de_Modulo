from .settings import *
import os

# SEGURIDAD
DEBUG = False

ALLOWED_HOSTS = [
    'tu-dominio.com',
    'www.tu-dominio.com',
    'tu-ip-servidor',
]

# Seguridad de cookies y sesiones
SESSION_COOKIE_SECURE = True  # Solo HTTPS
CSRF_COOKIE_SECURE = True  # Solo HTTPS
SECURE_SSL_REDIRECT = True  # Redirigir HTTP a HTTPS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Configuración de archivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Clave secreta - DEBE ser diferente en producción
# En producción, usar variable de entorno
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

# Base de datos - En producción usar PostgreSQL o MySQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME'),
#         'USER': os.environ.get('DB_USER'),
#         'PASSWORD': os.environ.get('DB_PASSWORD'),
#         'HOST': os.environ.get('DB_HOST'),
#         'PORT': os.environ.get('DB_PORT', '5432'),
#     }
# }

# Logging para producción
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django_errors.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}