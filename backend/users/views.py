from rest_framework.response import Response
from users.serializers import UserSerializer, UserProfileSerializer
from .models import User, UserProfile
from rest_framework import (
    generics, 
    mixins, 
    viewsets, 
    permissions, 
    views
)
from django.core.mail import send_mail
import string
import random
from django.shortcuts import redirect

## Работает

# Универсальное представление для работы с пользователями
# Создать пользователя - POST по адресу users (из urls.py) 
# + email, password в теле запроса (адрес везде без слеша на конце).
# Посмотреть одного пользователя - GET по адресу user/{id пользователя}.
# Посмотреть всех пользователей - GET по адресу users
from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.authtoken.models import Token
# from rest_framework.authtoken.models import Token

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
        u = request.user
        # user = self.get_object()
        queryset = self.queryset.filter(user=u,pk=pk)
        # token, created = Token.objects.get_or_create(user=user)
        # print(user.email, token.key)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

# Изменить поля в модели User методом PUT (чтобы изменить поля профиля, 
# надо писать в запросе "profile": {"first_name": "новое"}).
# !!!!profile добавлять обязательно! без него не работает, то есть
# { ... , profile: {}}  
class UserUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

# Сгенерировать пароль и отправить сообщение на указанную 
# почту с паролем. Регистрация пользователя с таким паролем 
# происходит отдельно (дополнительным запросом).
class SendInviteView(viewsets.ModelViewSet):
    # serializer_class = MessageSerializer

    def send_the_mail(self, request):
        email = request.data['email'] 
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        message_text = (
            'Вашу почту зарегистрировали на '
            + 'портале СЭД МТУСИ. Данные для '
            + 'входа:\nEmail: ' + email
            + '\nПароль: ' + password
            + '\nЕсли вам уже приходило подобное '
            + 'письмо, то данные в нем больше '
            + 'не действуют.'
        )

        send_mail(
            'Приглашение от СЭД МТУСИ',
            message_text,
            'nysha2161@gmail.com',
            [email,],
            fail_silently=False,
        )
        # u = UserViewSet.as_view({'get': 'list'})
        
        return Response({'password':password})

## Пока не работает, но будет

# class UserLogin(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     # permission_classes = (IsAdminUser,)

#     def list(self, request):
#         # Note the use of `get_queryset()` instead of `self.queryset`
#         queryset = self.get_queryset()
#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data)

# ## Эксперимент

# class Login(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

#     def login(self, request):
#         queryset = self.get_queryset()
#         print('queryset')
#         print(queryset)
#         u = obtain_jwt_token()
#         print(u)
#         return user

