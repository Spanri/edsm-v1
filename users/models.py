from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
# from docs.models import Doc

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "{}".format(self.email)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, blank=True)
    second_name = models.CharField(max_length=50, blank=True)
    patronymic = models.CharField(max_length=50, blank=True)
    position = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='media', blank=True)
    
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    def get_full_name(self):
        return self.first_name + " " + second_name + " " + patronymic

    post_save.connect(create_user_profile, sender=User)

class Notif(models.Model):
    user = models.ForeignKey(User, related_name="notif", on_delete=models.CASCADE)
    message = models.CharField(max_length=500, blank=True)
    date = models.DateField(blank=True, null=True)