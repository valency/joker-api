import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = "#p94vjet9clpl+iy6u#m$^lirp9vb3r9s_#*ho$2!+9g@ly=qy"
DEBUG = True
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "joker_auth",
    "joker_model",
    "joker_model_1",
    "joker_model_2",
    "joker_model_4",
    "joker_summary",
    "joker_tools",
    "joker_connector"
)

MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware"
)

ROOT_URLCONF = "joker.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "joker.wsgi.application"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "PAGE_SIZE": 10
}

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = ()

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

SQLITE_DIR = ""

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": SQLITE_DIR + "smartcube.db"
    },
    "joker_models": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "smartcube",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "5432",
        "APPS": ["joker_model", "joker_model_1", "joker_model_2", "joker_model_4"]
    },
    "joker_summary": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "OPTIONS": {
            "options": "-c search_path=summary_table"
        },
        "NAME": "smartcube",
        "SCHEMA": "summary_table",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "5432",
        "APPS": ["joker_summary"]
    }
}

DATABASE_ROUTERS = ["joker_common.routers.AuthRouter"]

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Hong_Kong"
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# HTTPS

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
