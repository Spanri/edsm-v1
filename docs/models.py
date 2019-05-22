from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# from users.models import User

class Doc(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    # owner = models.ForeignKey(User, related_name="docs", on_delete=models.CASCADE)
    file = models.FileField(blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    common = models.BooleanField(default=False)
    signature = models.CharField(max_length=255, blank=True, null=True)
