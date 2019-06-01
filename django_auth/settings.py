from botocore.exceptions import ClientError
import logging
import boto3
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'klc=#bj7qm#iiz%1ru-6y3%guc5_e(hq+3hm3&65dg6%c%@(*y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1',
                 'edms-mtuci.s3.amazonaws.com']

from corsheaders.defaults import default_methods
# CORS_ORIGIN_WHITELIST = (
#     'http//:localhost:8080',
# )
CORS_ORIGIN_ALLOW_ALL = True

# MEDIA_URL = STATIC_URL + 'media/'
# # STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )
# STATIC_ROOT = 'staticfiles/'
# # ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

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
    'storages',
    'users',
    'docs',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'django_auth.urls'



WSGI_APPLICATION = 'django_auth.wsgi.application'

#Database
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
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/static/')
# # STATIC_DIR = os.path.join(BASE_DIR, 'staticfiles/')
# # STATIC_URL = 'staticfiles/'
# STATICFILES_DIRS = (
#     # os.path.join(BASE_DIR, 'staticfiles/static/'),
#     os.path.join(BASE_DIR, 'frontend/dist/'),
# )
# MEDIA_ROOT = os.path.join(BASE_DIR, '')
# MEDIA_URL = '/'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAdminUser',
    )
}

# SMTP сервер
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'edmsmtuci@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get("EDMS-MAIL-PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Для создания связей моделей в БД
AUTH_USER_MODEL = 'users.User'

# Хероку
import django_heroku
django_heroku.settings(locals())


def create_bucket(bucket_name):
    """ Create an Amazon S3 bucket

    :param bucket_name: Unique string name
    :return: True if bucket is created, else False
    """

    # Let's use Amazon S3
    s3 = boto3.resource(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    )
    for bucket in s3.buckets.all():
        print(bucket.name)
    try:
        data = open('media/Ф123.doc', 'rb')
        s3.Bucket(bucket_name).put_object(Key='Ф1234.doc', Body=data)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# create_bucket('edms-mtuci')

# Для статических файлов, Amazon S3
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = 'us-east-1'
AWS_STORAGE_BUCKET_NAME = 'edms-mtuci'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
#AWS S3 Static
STATIC_URL = 'https://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'
# для автоматического collectstatic
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# для статики
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'storage_backends.StaticStorage'
# для медиа
MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'storage_backends.MediaStorage'
#
AWS_S3_FILE_OVERWRITE = False
# from django_auth import storage_backends

STATICFILES_DIRS = []
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
AWS_DEFAULT_ACL = None

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'staticfiles')],
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
