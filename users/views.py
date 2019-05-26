from rest_framework.response import Response
from users.serializers import (
    UserSerializer, 
    AuthTokenSerializer, 
    UserProfileSerializer,
    NotifSerializer,
)
from docs.serializers import (
    DocSerializer,
)
from .permissions import CustomIsAuthenticated
from .models import User, UserProfile, Notif
from docs.models import Doc
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
from itertools import chain

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

class Notif2(generics.ListAPIView):
    '''
    Нотифы конкретного пользователя, где он не владелец, 
    при этом документ может быть одним из:
    * доступен для просмотра, не надо подписывать (is_signature_request=0)
    * уже подписан (is_signature_request=1, is_signature=1)
    * надо подписать и очередь у него (is_signature_request=1, is_signature=0, is_queue=1)
    '''
    serializer_class = NotifSerializer
    queryset = Notif.objects.all()
    permission_classes = ()

    def get_queryset(self):
        notif = Notif.objects.filter(user_id=self.kwargs['pk'], is_owner=False)
        notif1 = notif.filter(is_signature_request=0)
        notif2 = notif.filter(is_signature_request=1, is_signature=1)
        notif3 = notif.filter(
            is_signature_request=1,
            is_signature=0, 
            is_queue=1
        )
        for i, n in enumerate(notif1):
            n2 = Notif.objects.get(is_owner=True, doc_id=n.doc_id)
            notif1[i].user = n2.user
            notif1[i].id = n2.id
        # Находим документы пользовтеля, которые подписали.
        # Сначала находим документы пользователя, которыми он владеет
        notif4 = Notif.objects.filter(user_id=self.kwargs['pk'], is_owner=True)
        # Для каждого документа проверяем, есть ли нотиф, где этот документ и 
        # is_owner=false, is_signature_request=true, is_signature=true
        for i, d in enumerate(notif4):
            try:
                d2 = Notif.objects.filter(
                    is_owner=False, 
                    doc_id=d.doc_id,
                    is_signature_request=True, 
                    is_signature=True
                )
                if d2:
                    notif1 = notif1.union(d2)
            except:
                pass
        # Добавляем нотифы, где пользователь - владелец
        notif5 = Notif.objects.filter(user_id=self.kwargs['pk'], is_owner=True)
        # Добавляем нотифы, где документы в общем доступе
        notif6 = Notif.objects.filter(user_id=self.kwargs['pk'], is_owner=True)
        # Объединяем (нотиф 4 присоединили отдельно выше)
        notif1 = notif1.union(notif2).union(notif3).union(notif5).union(notif6)
        return notif1

class AddSignature(viewsets.ModelViewSet):
    '''
    Добавить подпись к документу. Принимает id документа.
    '''
    serializer_class = DocSerializer
    queryset = Doc.objects.all()
    permission_classes = ()

    def add_signature(self, request):
        # Найти нужный документ
        doc = Doc.objects.get(id=request.data['id'])

        # Тут должна быть функция генерации подписи
        signature = "123456"

        # Добавить подпись
        doc.signature = signature
        doc.save()
        
        # Найти нотиф, который с этим документом и 
        # где очередь подписывать и изменить на "подписано"
        notif = Notif.objects.get(
            doc_id=doc.id, 
            is_owner=False,
            is_signature_request=1, 
            is_queue=True
        )
        notif.is_queue = False
        notif.is_signature = True
        notif.message = "Ваш документ подписали."
        notif.is_show_notif = True
        notif.save()

        # Найти следующий нотиф, который с этим документом и
        # где очередь = очередь+1
        try:
            notifNext = Notif.objects.get(
                doc_id=doc.id,
                is_owner=False,
                is_signature_request=1,
                queue=notif.queue+1
            )
            print(notifNext)
            notifNext.is_queue = True
            notif.message = "Вас просят подписать документ."
            notifNext.save()
        except:
            pass

        serializer = DocSerializer(doc)
        return Response(serializer.data)

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

# ## Не нужно, но жалко выкидывать

# class Notif1(generics.ListAPIView):
#     '''
#     Нотифы конкретного пользователя, где он не владелец
#     '''
#     serializer_class = NotifSerializer
#     queryset = Notif.objects.all()
#     permission_classes = ()

#     def get_queryset(self):
#         return Notif.objects.filter(is_owner=False)

# class DocsOwner(generics.ListAPIView):
#     '''
#     Нотифы конкретного пользователя, где пользователь
#      - владелец документов.
#     '''
#     serializer_class = NotifSerializer
#     queryset = Notif.objects.all()
#     permission_classes = ()

#     def get_queryset(self):
#         return Notif.objects.filter(user_id=self.kwargs['pk'], is_owner=True)

# class DocsOwnerOne(generics.ListAPIView):
#     '''
#     Нотиф конкретного докумена, где юзер -
#     владелец документа.
#     '''
#     serializer_class = NotifSerializer
#     queryset = Notif.objects.all()
#     permission_classes = ()

#     def get(self, request, pk, format=None):
#         try:
#             n = Notif.objects.get(doc_id=self.kwargs['pk'], is_owner=True)
#             serializer = NotifSerializer(n)
#             return Response(serializer.data)
#         except:
#             return Response({})

# class AllDocs(generics.ListAPIView):
#     '''
#     Все нотифы, которые в общем доступе и
#     обозначают владельца.
#     '''
#     serializer_class = NotifSerializer
#     queryset = Notif.objects.all()
#     permission_classes = ()
#     def get_queryset(self):
#         return Notif.objects.filter(doc__common=True, is_owner=True)

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
