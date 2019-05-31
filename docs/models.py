from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class FileCabinet(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

class Doc(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to='media', blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    common = models.BooleanField(default=False)
    signature = models.CharField(max_length=255, blank=True, null=True)
    fileCabinet = models.ForeignKey(FileCabinet, related_name="doc",
                                    on_delete=models.CASCADE, default=1)
