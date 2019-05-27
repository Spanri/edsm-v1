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
import datetime

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
            'profile',
        )

    def create(self, validated_data):
        profile_data = dict(validated_data.get('profile'))
        user_data = dict(validated_data)
        del user_data['profile']
        user = User.objects.create(**user_data)
        user.set_password(user_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        try:
            # print(validated_data)
            if('password' in validated_data):
                instance.set_password(validated_data['password'])
                instance.save()
                validated_data.pop('password')
            if('profile' in validated_data):
                nested_serializer = self.fields['profile']
                nested_instance = instance.profile
                nested_data = validated_data.pop('profile')
                # print(nested_instance)
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

    class Meta:
        model = Notif
        fields = (
            'id',
            'user_id',
            'doc_id',
            'date',
            'is_owner',
            'is_signature_request',
            'is_signature',
            'is_show_notif',
            'queue',
            'is_queue',
            'user',
            'doc'
        )
        unique_together = (("user_id", "doc_id"),)

    def create(self, validated_data):
        now = datetime.datetime.now()
        notif = Notif.objects.create(**validated_data)
        notif.date = now.strftime("%Y-%m-%d")
        notif.save()
        return notif
    
    # def get_object(self, pk):
    #     return TestModel.objects.get(pk=pk)

    # def patch(self, request, pk):
    #     notif = self.get_object(pk)
    #     serializer = NotifModelSerializer(
    #         notif, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonReponse(code=201, data=serializer.data)
    #     return JsonResponse(code=400, data="wrong parameters")
    
    def update(self, instance, validated_data):
        try:
            if('doc' in validated_data):
                nested_serializer = self.fields['doc']
                nested_instance = instance.doc
                nested_data = validated_data.pop('doc')
                nested_serializer.update(nested_instance, nested_data)
                return nested_serializer.update(instance, validated_data)
            else:
                return super(UserSerializer, self).update(instance, validated_data)
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
        
