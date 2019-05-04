from rest_framework.response import Response
from users.serializers import UserSerializer, UserProfileSerializer
from .models import User, UserProfile
from .permissions import IsAdmin
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
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# from rest_framework.authtoken.models import Token

## Работает

# Универсальное представление для работы с пользователями
# Создать пользователя - POST по адресу users (из urls.py) 
# + email, password в теле запроса (адрес везде без слеша на конце).
# Посмотреть одного пользователя - GET по адресу user/{id пользователя}.
# Посмотреть всех пользователей - GET по адресу users
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = []
    permission_classes = []

# Изменить поля в модели User методом PUT (чтобы изменить поля профиля, 
# надо писать в запросе "profile": {"first_name": "новое"}).
# !!!!profile добавлять обязательно! без него не работает, то есть
# { ... , profile: {}}  
class UserUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

# Сгенерировать пароль и отправить сообщение на указанную 
# почту с паролем. Регистрация пользователя с таким паролем 
# происходит отдельно (дополнительным запросом).
class SendInviteView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdmin,)

    def send_the_mail(self, request):
        # authentication_classes = (TokenAuthentication,)
        # permission_classes = (IsAdmin,)
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
        
        return Response({'password':password})

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
    # def retrieve(self, request, *args, **kwargs):
    #     user = self.get_object()
    #     token, created = Token.objects.get_or_create(user=user)
    #     serializer = self.get_serializer(user)
    #     return Response({
    #         'token': token.key,
    #         **serializer.data
    #     })

