from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid
from django.db.models.signals import post_save, post_delete
# Для FTP сервера
from ftp import FTPStorage
fs = FTPStorage()

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

class Reg(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)

class Block(models.Model):
    data = models.CharField(max_length=500, blank=True, null=True)
    hash = models.CharField(max_length=500, blank=True, null=True)
    previous_hash = models.CharField(max_length=500, blank=True, null=True)

class Doc(models.Model):
    reg = models.ForeignKey(Reg, related_name="doc_reg",
                            on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to='./docs/', storage=fs, blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    common = models.BooleanField(default=False)
    signature = models.CharField(max_length=500, blank=True, null=True)
    signature_end = models.BooleanField(default=False)
    hash = models.ForeignKey(Block, related_name="doc_h",
                             on_delete=models.CASCADE, blank=True, null=True)
    cancel_description = models.CharField(max_length=500, blank=True, null=True)
    cancel_file = models.FileField(
        upload_to='./cancel_docs/', storage=fs, blank=True, null=True)
    file_cabinet = models.ForeignKey(FileCabinet, related_name="doc_fc",
                                     on_delete=models.CASCADE, blank=True, null=True)

    post_delete.connect(receiver=delete_doc)
