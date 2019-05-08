from .models import User, UserProfile
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = UserProfile
        fields = (
            'id',
            'first_name',
            'second_name', 
            'patronymic',
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
        profile_data =  dict(validated_data.get('profile'))
        user_data = dict(validated_data)
        del user_data['profile']
        user = User.objects.create(**user_data)
        user.set_password(user_data['password'])
        user.save()
        UserProfile.objects.create(user=user,**profile_data)
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        validated_data.pop('password')
        nested_serializer = self.fields['profile']
        nested_instance = instance.profile
        nested_data = validated_data.pop('profile')
        print(instance.password)
        nested_serializer.update(nested_instance, nested_data)
        return nested_serializer.update(instance, validated_data)

# Вроде можно убрать, но на всякий случай
users = User.objects.all()
for user in users:
    token, created = Token.objects.get_or_create(user=user)
    print(user.email, token.key)

from django.core import exceptions

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