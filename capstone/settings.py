import os
from dotenv import load_dotenv
from pathlib import Path
import sys
# Load environment variables from .env file
load_dotenv()




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Access environment variables
SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')

EMAILJS_USER_ID = os.environ.get("EMAILJS_USER_ID")
EMAILJS_SERVICE_ID = os.environ.get("EMAILJS_SERVICE_ID")
EMAILJS_TEMPLATE_ID = os.environ.get("EMAILJS_TEMPLATE_ID")


DEBUG = False

# Properly load ALLOWED_HOSTS from .env
ALLOWED_HOSTS = [

    'cms-version1-0.onrender.com',
    'news-version1-0.onrender.com',
    'localhost', 
    '127.0.0.1',
    'glitch-cms.motherboard.live',
    'news.motherboard.live'
]

# Add CSRF_TRUSTED_ORIGINS (required for Django 4.0+)
CSRF_TRUSTED_ORIGINS = [

    'https://cms-version1-0.onrender.com',
    'https://news-version1-0.onrender.com',
    'https://glitch-cms.motherboard.live',
    'https://news.motherboard.live',
    'http://localhost',
    'http://127.0.0.1',
]

# Additional CSRF settings that might help

CSRF_COOKIE_SECURE = True  # Set to False if not using HTTPS
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = False

# Application definition

INSTALLED_APPS = [
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tinymce",
    "cms",
    "news",
    "haystack",
    "clearcache",
    'crispy_forms',
    "crispy_bootstrap5",
    "simple_history",
    'allauth',
    'storages',
    'allauth.account',
    'allauth.socialaccount',  
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)


AWS_ACCESS_KEY_ID = os.getenv("DO_SPACES_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("DO_SPACES_SECRET")
AWS_STORAGE_BUCKET_NAME = os.getenv("DO_SPACES_NAME")
AWS_S3_ENDPOINT_URL = f'https://{os.getenv("DO_SPACES_REGION")}.digitaloceanspaces.com'


MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.{os.getenv("DO_SPACES_REGION")}.digitaloceanspaces.com/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_QUERYSTRING_AUTH = True



ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True  


AUTH_PROFILE_MODULE = 'news.Profile'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_FAIL_SILENTLY = not DEBUG

MIDDLEWARE = [
    "allauth.account.middleware.AccountMiddleware",
    'simple_history.middleware.HistoryRequestMiddleware',
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "capstone.urls"

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

HAYSTACK_DOCUMENT_FIELD = 'text'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = "capstone.wsgi.application"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = "news.User"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'cms', 'static'),
    os.path.join(BASE_DIR, 'news', 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
