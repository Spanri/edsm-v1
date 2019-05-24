from rest_framework.response import Response
from users.serializers import (
    UserSerializer, 
    AuthTokenSerializer, 
    UserProfileSerializer,
    NotifSerializer
)
from .permissions import CustomIsAuthenticated
from .models import User, UserProfile, Notif
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
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.views.generic import TemplateView
from django.core import exceptions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import parsers, renderers

## Работает
class Index(TemplateView):
    '''
    Шаблон, показывает vue приложение на сервере.
    '''
    template_name = "index.html"
    permission_classes = ()

    def get_context_data(self):
        context = super(Index, self).get_context_data()
        return context


class NotifViewSet2(generics.ListAPIView):
    '''
    Унив
    '''
    serializer_class = NotifSerializer
    queryset = Notif.objects.all()
    permission_classes = ()

    def get_queryset(self):
        notif = Notif.objects.filter(user_id=self.kwargs['pk'], owner=False)
        for n in notif:
            old_message = n.message
            n = Notif.objects.get(doc_id=n.doc_id, owner=True)
            n.message = old_message
            print(n)
        return notif

class DocsOwnerViewSet(generics.ListAPIView):
    '''
    Возвр
    '''
    serializer_class = NotifSerializer
    queryset = Notif.objects.all()
    permission_classes = ()

    def get_queryset(self):
        return Notif.objects.filter(user_id=self.kwargs['pk'],owner=True)


class DocsOwnerOneViewSet(generics.ListAPIView):
    '''
    Возвр
    '''
    serializer_class = NotifSerializer
    queryset = Notif.objects.all()
    permission_classes = ()

    def get(self, request, pk, format=None):
        n = Notif.objects.get(doc_id=self.kwargs['pk'], owner=True)
        serializer = NotifSerializer(n)
        return Response(serializer.data)

class AllDocsViewSet(generics.ListAPIView):
    '''
    Возвр
    '''
    serializer_class = NotifSerializer
    queryset = Notif.objects.all()
    permission_classes = ()
    def get_queryset(self):
        # user_id = self.kwargs['pk'],
        return Notif.objects.filter(doc__common=True)

# class GetEmail(generics.ListAPIView):
#     '''
#     Получение списка всех email и имен.
#     '''
#     permission_classes = ()
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

#     def get(self, *args, **kwargs):
#         u = User.objects.get(id=self.kwargs['pk'])
#         uu = UserProfile.objects.get(user_id=u.id)
#         return Response({"full_name": uu.get_full_name()})

class ObtainAuthToken(views.APIView):
    '''
    Переопределение получения токена, потому что по дефолту он 
    получается через username и пароль, а надо через email и пароль.
    '''
    title="123456"
    description = "dfdgf"
    throttle_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})

class UserViewSet(viewsets.ModelViewSet):
    '''
    Универсальное представление для работы с пользователями.
    (адрес без слеша в конце, где список получать)
    '''
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticated,)

class NotifViewSet(viewsets.ModelViewSet):
    '''
    Универсальное представление для работы с пользователями.
    (адрес без слеша в конце, где список получать)
    '''
    serializer_class = NotifSerializer
    queryset = Notif.objects.all()
    permission_classes = ()

    def get_queryset(self):
        return Notif.objects.filter(owner=False)

class UserFromTokenViewSet(viewsets.ModelViewSet):
    '''
    Получить id по токену.
    '''
    serializer_class = UserSerializer
    permission_classes = ()

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

class SendInviteView(viewsets.ModelViewSet):
    '''
    Сгенерировать пароль и отправить сообщение на указанную 
    почту с паролем. Принимает email, возвращает пароль.\n
    Регистрация пользователя с таким паролем 
    происходит отдельно (дополнительным запросом).
    Доступ к функции имеют только аккаунты с is_staff = true
    (аккаунт берется из посланного токена)
    '''
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    def send_the_mail(self, request):
        email = request.data['email']
        is_staff = request.data['is_staff']
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
            'edmsmtuci@gmail.com',
            [email,],
            fail_silently=False,
        )

        user = User.objects.create_user(
            email = email,
            password = password,
            username = email,
            is_staff = is_staff
        )
        UserProfile.objects.filter(user_id=user.id).update(
            second_name = email,
            position = "Должность не указана"
        )
        user.save()
        
        return Response({'password':password})

# проверить наличие почты в бд, потом отправить email
class ConfirmUpdatePasswordView(viewsets.ModelViewSet):
    '''
    Отправить подтверждение смены пароля с кодом
    подтверждения. Принимает email, возвращает ничего.\n
    Регистрация пользователя с таким паролем 
    происходит отдельно (дополнительным запросом).
    Доступ к функции имеют только аккаунты с is_staff = true
    (аккаунт берется из посланного токена)
    '''
    serializer_class = UserSerializer
    permission_classes = ()
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
        
    def confirm_update_password(self, request):
        email = request.data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            content = {'error': 'Пользователь не создан.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        message_text = (
            'Код подтверждения: ' + code
            + '\nВведите его в форму для изменения пароля.'
        )

        send_mail(
            'Смена пароля от СЭД МТУСИ',
            message_text,
            'edmsmtuci@gmail.com',
            [email,],
            fail_silently=False,
        )
        
        return Response({"code": code})

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

# class UserUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
#     '''
#     Изменить поля в модели User методом PUT (чтобы изменить поля профиля, 
#     надо писать в запросе "profile": {"first_name": "новое"}).\n
#     Поле profile добавлять обязательно (даже если пустое - {})! без 
#     него не работает. Кроме того, пользователь должен существовать. 
#     '''
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
