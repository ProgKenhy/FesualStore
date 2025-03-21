import os
from pathlib import Path
import socket
import sys
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

DOMAIN_NAME = os.getenv('DOMAIN_NAME', 'http://localhost:8000')
YANDEX_METRICA_ID = os.getenv('YANDEX_METRICA_ID')

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False").lower() == 'true'

TESTING = "test" in sys.argv

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# CSRF
CSRF_TRUSTED_ORIGINS = ['https://fesualstore.ru', 'https://www.fesualstore.ru']

# Application definitions
INSTALLED_APPS = [
    # external apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'channels',
    # 'allauth.socialaccount.providers.vk',
    'django_filters',
    'phonenumber_field',

    # internal apps
    "products",
    "users",
    "orders",
    "information",
    'support',

    # default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.humanize',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    'allauth.account.middleware.AccountMiddleware',
]

if not TESTING:
    INSTALLED_APPS = [*INSTALLED_APPS, "debug_toolbar"]
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        *MIDDLEWARE,
    ]

ROOT_URLCONF = "config.urls"

# Starting with Django 4.1+ we need to pick which template loaders to use
# based on our environment since 4.1+ will cache templates by default.
default_loaders = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

cached_loaders = [("django.template.loaders.cached.Loader", default_loaders)]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                'config.context_processors.allowed_hosts',
                'config.context_processors.metrika_id',
                'products.context_processors.categories',
                'products.context_processors.baskets',
            ],
            "loaders": default_loaders if DEBUG else cached_loaders,
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "store"),
        "USER": os.getenv("POSTGRES_USER", "store"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "password"),
        "HOST": os.getenv("POSTGRES_HOST", "postgres"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa: E501
    },
]

# Sessions
# https://docs.djangoproject.com/en/5.0/ref/settings/#sessions
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

# Redis and Celery
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TASK_TIME_LIMIT = 30 * 60
# CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Caching
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Kaliningrad"
USE_I18N = True
# USE_L10N = True
USE_TZ = True


MEDIA_ROOT = os.path.join(BASE_DIR, "..", "media")
MEDIA_URL = "/media/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "..", "public")]
STATIC_ROOT = os.path.join(BASE_DIR, "..", "public_collected")

# Настройки хранилищ
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage" if not DEBUG
                  else "whitenoise.storage.StaticFilesStorage",
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": MEDIA_ROOT,
        },
    },
}

# Автоматическое обновление статики в режиме разработки
WHITENOISE_AUTOREFRESH = DEBUG


# Django Debug Toolbar
# https://django-debug-toolbar.readthedocs.io/
if DEBUG:
    # We need to configure an IP address to allow connections from, but in
    # Docker we can't use 127.0.0.1 since this runs in a container but we want
    # to access the toolbar from our browser outside of the container.
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]

# Users

AUTH_USER_MODEL = 'users.User'
ACCOUNT_FORMS = {
    'signup': 'users.forms.UserLoginForm',  # Укажите путь к вашей кастомной форме
}
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Sending emails

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_FILE_PATH = BASE_DIR / "sent_emails"
    # CELERY_TASK_ALWAYS_EAGER = True
    # CELERY_TASK_EAGER_PROPAGATES = True
else:
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = os.getenv('EMAIL_PORT')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

    EMAIL_SERVER = EMAIL_HOST_USER
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == 'True'  # Convert to boolean
    EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL') == 'True'  # Convert to boolean

    if EMAIL_USE_TLS and EMAIL_USE_SSL:
        raise ValueError("EMAIL_USE_TLS and EMAIL_USE_SSL are mutually exclusive. Set only one to True.")

# OAuth

AUTHENTICATION_BACKENDS = [

    # Needed to log by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
            'user:email',
        ],
    }
}

SOCIALACCOUNT_QUERY_EMAIL = True

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

# Channels
ASGI_APPLICATION = "config.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s [%(asctime)s] [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'json': {
            'format': '%(message)s',
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '''
                {
                    "timestamp": "%(asctime)s",
                    "level": "%(levelname)s",
                    "name": "%(name)s",
                    "line": "%(lineno)s",
                    "message": "%(message)s"
                }
            ''',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'json_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.getenv('LOG_LEVEL', 'INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_SERVER_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_DB_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_REQUEST_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'channels': {
            'handlers': ['console'],
            'level': os.getenv('CHANNELS_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'support': {
            'handlers': ['console'],
            'level': os.getenv('SUPPORT_LOG_LEVEL', 'DEBUG'),
            'propagate': False,
        },
    },
}

# Automatically switch to JSON logging in production for better log aggregation
if not DEBUG:
    for logger_name in LOGGING['loggers']:
        if 'console' in LOGGING['loggers'][logger_name]['handlers']:
            LOGGING['loggers'][logger_name]['handlers'] = ['json_console']

    if 'console' in LOGGING['root']['handlers']:
        LOGGING['root']['handlers'] = ['json_console']
