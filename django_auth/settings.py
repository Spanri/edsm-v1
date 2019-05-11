import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Хероку
# import django_heroku
# django_heroku.settings(locals())

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'klc=#bj7qm#iiz%1ru-6y3%guc5_e(hq+3hm3&65dg6%c%@(*y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
if DEBUG:
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

from corsheaders.defaults import default_methods
# CORS_ORIGIN_WHITELIST = (
#     'http//:localhost:8080',
# )
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = default_methods + (
    'PUT', 'PATCH'
)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_rest_passwordreset',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'django_auth.urls'

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

WSGI_APPLICATION = 'django_auth.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Для 
REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER': 
        'users.serializers.PasswordResetSerializer',
}


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# Для деплоймента
STATIC_ROOT = os.path.join(BASE_DIR, 'public/')
# Для 
STATIC_URL = 'frontend/dist/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'frontend/dist/'),
)
MEDIA_URL = "media/"
MEDIA_ROOT = "media/"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.IsAdminUser',
    )
}

# SMTP сервер
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'edmsmtuci@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get("EDMS-MAIL-PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Для файлов
MEDIA_ROOT = os.path.join(BASE_DIR, '')
MEDIA_URL = '/'

# Не помню точно зачем, но надо
AUTH_USER_MODEL = 'users.User'

