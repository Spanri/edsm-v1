from .models import User, UserProfile, Notif
from docs.serializers import DocSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core import exceptions
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.core import exceptions
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from django.core.mail import send_mail, EmailMessage
import boto3
import os
from django.template.loader import get_template

def send_notif(notif):
    notifOwner = Notif.objects.get(
        doc_id=notif.doc.id,
        status=0
    )
    if notif.user.is_get_notif_email:
        if (notifOwner.user.profile.first_name != "" and notifOwner.user.profile.patronymic != ""):
            full_name = notifOwner.user.profile.second_name + " " + \
                notifOwner.user.profile.first_name[0] + \
                "." + notifOwner.user.profile.patronymic[0] + "."
        else:
            full_name = notifOwner.user.profile.second_name
        message = (
            '<p>Пользователь ' + full_name + ' (' + notifOwner.user.email + ') просит вас подписать документ "' +
            notif.doc.title + '".</p><p>Пожалуйста, зайдите в систему СЭД МТУСИ, чтобы принять решение, подписать ' +
            'документ или отклонить.</p><a href="https://edms-mtuci.herokuapp.com/document/' +
            str(notif.doc.id) + '">https://edms-mtuci.herokuapp.com/document/' +
            str(notif.doc.id) +
            '</a><p>Отключить получение уведомлений на почту можно в настройках профиля.</p>'
        )
        msg = EmailMessage(
            'Вас просят подписать документ, СЭД МТУСИ',
            message,
            'edmsmtuci@gmail.com',
            [notif.user.email, ],
        )
        msg.content_subtype = "html"
        # Скачиваем файл из хранилища
        s3 = boto3.resource(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get(
                'AWS_SECRET_ACCESS_KEY'),
        )
        s3.meta.client.download_file(
            'edms-mtuci',
            'media/' + str(notif.doc.file),
            'staticfiles/media/' + str(notif.doc.file)
        )
        msg.attach_file('staticfiles/media/' + str(notif.doc.file))
        msg.send()

class UserProfileSerializer(serializers.HyperlinkedModelSerializer): 
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        if (obj.first_name != "" and obj.patronymic != ""):
            return obj.second_name + " " + obj.first_name[0] + "." + obj.patronymic[0] + "."
        else:
            return obj.second_name

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'first_name',
            'second_name',
            'patronymic',
            'full_name',
            'position',
            'photo',
        )

class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'date_joined',
            'is_staff',
            'is_get_notif_email',
            'is_get_notif_expired_email',
            'profile',
        )

    # создает профиль, но не отображает его
    def create(self, validated_data):
        profile_data = dict(validated_data.get('profile'))
        user_data = dict(validated_data)
        del user_data['profile']
        user = User.objects.create(**user_data)
        user.set_password(user_data['password'])
        userProfile = UserProfile.objects.filter(user_id=user.id)
        userProfile.update(**profile_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        try:
            if('password' in validated_data):
                instance.set_password(validated_data['password'])
                instance.save()
                validated_data.pop('password')
            if('profile' in validated_data):
                nested_serializer = self.fields['profile']
                nested_instance = instance.profile
                # if('photo' in nested_serializer):
                #     uP = UserProfile.objects.get(id=nested_instance.id)
                #     image = Image.open(uP.photo.path)
                #     image.save(uP.image.path, quality=20, optimize=True)
                nested_data = validated_data.pop('profile')
                nested_serializer.update(nested_instance, nested_data)
                return nested_serializer.update(instance, validated_data)
            else:
                return super(UserSerializer, self).update(instance, validated_data)
        except:
            content = {'error': 'Something else went wrong'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class NotifSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(required=False)
    doc = DocSerializer(required=False)
    user_id = serializers.IntegerField(write_only=True)
    doc_id = serializers.IntegerField(write_only=True)
    is_read = UserSerializer(required=False, many=True)
    is_read_id = UserSerializer(required=False, many=True)

    class Meta:
        model = Notif
        fields = (
            'id',
            'user_id',
            'doc_id',
            'is_read_id',
            'date',
            'date_expire',
            'is_notif_expire',
            'status',
            'queue',
            'is_read',
            'user',
            'doc'
        )
        unique_together = (("user_id", "doc_id"),)

    def create(self, validated_data):
        # Создаем нотиф и указываем текущее время, сохраняем
        notif = Notif.objects.create(**validated_data)
        notif.date = timezone.now()
        notif.save()

        # Проверяем, есть ли статус 2. Если да, отправляем
        # пользователю уведомление на почту.
        if notif.status == 2:
            send_notif(notif)

        return notif
    
    def update(self, instance, validated_data):
        try:
            if('doc' in validated_data):
                nested_serializer = self.fields['doc']
                nested_instance = instance.doc
                nested_data = validated_data.pop('doc')
                nested_serializer.update(nested_instance, nested_data)
                return nested_serializer.update(instance, validated_data)
            else:
                return super(NotifSerializer, self).update(instance, validated_data)
        except:
            content = {'error': 'Something else went wrong'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

class AuthTokenSerializer(serializers.Serializer):
    '''
    Переопределение получения токена, потому что по дефолту он 
    получается через username и пароль, а надо через email и пароль. 
    '''
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to log in with provided credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Must include "email" and "password".'
            raise exceptions.ValidationError(msg)

        data['user'] = user
        return data

class PasswordResetSerializer(serializers.Serializer):
    '''
    Переопределение сброса пароля для красивого отображения email.
    '''
    email = serializers.EmailField()
    password_reset_form_class = PasswordResetForm
    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Error'))

        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('Invalid e-mail address'))
        return value

    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'email_template_name': 'registration/password_reset_email.html',
            'request': request,
        }
        self.reset_form.save(**opts)
        
