from pathlib import Path
import environ
from .base import *

env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db name',
        'USER': 'db user',
        'PASSWORD': 'db password',
        'HOST': 'db host',
        'PORT': 'db port'
    }
}

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)
