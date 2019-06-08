from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid
from django.db.models.signals import post_save, post_delete

def delete_doc(sender, **kwargs):
    '''
    функция удаления документов при удалении объектов
    '''
    try:
        object_ = kwargs.get('instance')
        storage, path = object_.file.storage, object_.file.path
        print(path)
        storage.delete(path)
    except:
        pass

class FileCabinet(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

class Doc(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to='', blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    common = models.BooleanField(default=False)
    signature = models.CharField(max_length=500, blank=True, null=True)
    cancel_description = models.CharField(max_length=500, blank=True, null=True)
    cancel_file = models.FileField(upload_to='', blank=True, null=True)
    file_cabinet = models.ForeignKey(FileCabinet, related_name="doc",
                                    on_delete=models.CASCADE, default=1)

    post_delete.connect(receiver=delete_doc)
