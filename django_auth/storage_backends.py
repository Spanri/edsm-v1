from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
	location = settings.AWS_STATIC_LOCATION


class MediaStorage(S3Boto3Storage):
	location = settings.AWS_MEDIA_LOCATION
	# To turn access control list into private use only. Will use it in models.py
	default_acl = 'public'
	file_overwrite = False  # Not to replace files even they have same name
	custom_domain = False


class PublicStorage(S3Boto3Storage):
	location = settings.AWS_PUBLIC_LOCATION
	file_overwrite = False
