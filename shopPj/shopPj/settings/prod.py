import os
from .base import *
from dotenv import load_dotenv


load_dotenv(os.path.join(BASE_DIR, '.env'))


DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_DB_PORT'),
    }
}

# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
