from .base import *
import os

# SECRET_KEY=os.environ.get("SECRET_KEY")
# DEBUG=False
# ALLOWED_HOSTS=['*']


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "hello_django_dev",
        "USER": "hello_django",
        "PASSWORD": "hello_django",
        "HOST": "db",
        "PORT": "5432",
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
