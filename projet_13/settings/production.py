import environ
from .base import *
import dj_database_url


env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env("SECRET_KEY")

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "db name",
        "USER": "db user",
        "PASSWORD": "db password",
        "HOST": "db host",
        "PORT": "db port",
    }
}

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES["default"].update(db_from_env)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('HOST_EMAIL')
EMAIL_HOST_PASSWORD = env('HOST_PASSWORD')