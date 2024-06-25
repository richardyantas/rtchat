from .base import *
import os

# SECRET_KEY=os.environ.get("SECRET_KEY")
# DEBUG=False
# ALLOWED_HOSTS=['*']

# DATABASES={
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.environ.get("SQL_DATABASE"),
#         "USER": os.environ.get("SQL_USER"),
#         "PASSWORD": os.environ.get("SQL_PASSWORD"),
#         "HOST": os.environ.get("SQL_HOST"),
#         "PORT": os.environ.get("SQL_PORT"),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

