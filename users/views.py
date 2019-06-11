from django.core.files.base import ContentFile
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
from docs.permissions import (
    CustomIsAuthenticated as CustomIsAuthenticatedDoc,
)
from .permissions import (
    CustomIsAuthenticated,
    CustomIsAuthenticated2,
    CustomIsAuthenticated3,
    CustomIsAuthenticated4,
)
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
import copy

## Работает
class Index(TemplateView):
    '''
    Шаблон, показывает vue приложение на сервере.
    Права - нет.
    '''
    template_name = "index.html"
    # template_name = 'https://edms-mtuci.s3.amazonaws.com/static/index.html'
    permission_classes = ()

    def get_context_data(self):
        context = super(Index, self).get_context_data()
        return context

def unique(list1):  
    unique_list = [] 
    for x in list1:
        if x not in unique_list: 
            unique_list.append(x)
    return unique_list
    
class Notif2(generics.ListAPIView):
    '''
    Нотифы конкретного пользователя
    1. где он не владелец, при этом документ может быть одним из:
        + доступен для просмотра, не надо подписывать (is_signature_request=0)
        + уже подписан (is_signature_request=1, is_signature=1)
        + надо подписать и очередь у него (is_signature_request=1, is_signature=0, is_queue=1)
    2. где он владелец
    3. где документы в общем доступе
    Права - владелец или админ.
    '''
    serializer_class = NotifSerializer
    queryset = Notif.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticated2,)

    def list(self, request, *args, **kwargs):
        print('a-1')
        notif = super(Notif2, self).list(request, args, kwargs)
        notif2 = []
        notif_owner = []
        notif_common = []
        user_id = int(self.kwargs['pk'])
        print('a0')
        for i, n in enumerate(notif.data):
            d = {}
            for idx, val in enumerate(n):
                d.setdefault(val, n[val])
            notif.data[i] = d
            # надо подписать и очередь или
            # подписан и есть уведомления или
            # отклонил документ
            # просто смотрю, не надо подписывать
            if(
                (
                    n['user']['id'] == user_id and
                    (
                        n['status'] == 2 or
                        n['status'] == 3
                    )
                ) or (
                    n['user']['id'] == user_id and
                    n['doc']['signature_end'] == True and
                    n['status'] == 5
                )
            ):
                notif2.append(notif.data[i])
            # владелец (отдельно, ибо нужно дальше)
            if(
                n['user']['id'] == user_id and
                n['status'] == 0
            ):
                notif_owner.append(notif.data[i])
            # документ в общем доступе
            if(
                n['doc']['common'] and
                n['doc']['signature_end'] == True and
                n['status'] == 0
            ):
                notif2.append(notif.data[i])
        notif2 = notif2 + notif_owner
        # Находим документы пользователя, которые подписали, чтобы
        # вывести это в уведомления с сообщением "Ваш документ подписали."
        # Для каждого документа, где пользователь - владелец, проверяем,
        # есть ли нотиф, где этот документ и он (подписан или отклонен)
        notif_signature = []
        for i, n in enumerate(notif_owner):
            for j, n2 in enumerate(notif.data):
                if(
                    n2['doc']['id'] == n['doc']['id'] and
                    (
                        n2['status'] == 3 or
                        n2['status'] == 7
                    )
                ):
                    notif_signature.append(n2)
                    break
        notif2 = notif2 + notif_signature
        for i, n in enumerate(notif2):
            for j, n2 in enumerate(notif2):
                # Если подписал сам владелец, то пусть будет
                # статус = 6 (в таблице оригинальной он нигде не занят)
                if(
                    n2['user']['id'] == user_id and
                    (n2['status'] == 3 or n2['status'] == 4)
                ):
                    notif2[j]['status'] = 6
                    break
        notif3 = copy.deepcopy(notif.data)
        # Ищем все "мои документы", потом для каждого "моего
        # документа" пытаемся найти нотиф с тем же документом и
        # который надо подписать другому пользователю 
        # ДОЛГО ДЕЛАЕТСЯ
        for i, n in enumerate(notif2):
            notif2[i]['initiator'] = ''
            if n['status'] == 0:
                for j, n2 in enumerate(notif3):
                    if (
                        n2['doc']['id'] == n['doc']['id'] and
                        n2['status'] == 2
                    ):
                        notif2[i]['initiator'] = n2['user']
                        break
        # Заменяем не владельцев на владельцев
        for i, n in enumerate(notif3):
            for j, n2 in enumerate(notif3):
                if (
                    n2['doc']['id'] == n['doc']['id'] and
                    n2['status'] == 0
                ):
                    for k, n3 in enumerate(notif2):
                        if (
                            n3['doc']['id'] == n['doc']['id']
                        ):
                            notif2[k]['user'] = notif3[j]['user']
                            break
                    break
        notif2 = unique(notif2)
        print('a2.9')
        return Response(notif2)

class NotifQueue(generics.ListAPIView):
    '''
    У кого сейчас очередь подписывать этот документ.
    Права - владелец документа или админ.
    '''
    serializer_class = NotifSerializer
    queryset = Notif.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticatedDoc,)

    def get_queryset(self):
        doc = Doc.objects.get(id=self.kwargs['pk'])
        notif = Notif.objects.filter(
            doc_id=doc.id,
            status=2
        )
        return notif

class ObtainAuthToken(views.APIView):
    '''
    Переопределение получения токена, потому что по дефолту он 
    получается через username и пароль, а надо через email и пароль.
    Права - нет.
    '''
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
    Права - админ или владелец аккаунта.
    '''
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticated,)

class GetEmails(generics.ListAPIView):
    '''
    Все емайлы
    Права - нет.
    '''
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = ()

    def list(self, request, *args, **kwargs):
        users = super(GetEmails, self).list(request, args, kwargs)
        for i, n in enumerate(users.data):
            users.data[i] = {
                "id": users.data[i]['id'],
                "full_name": users.data[i]['profile']['full_name'],
                "position": users.data[i]['profile']['position'],
            }
        return Response(users.data)

class NotifViewSet(viewsets.ModelViewSet):
    '''
    Универсальное представление для работы с пользователями.
    (адрес без слеша в конце, где список получать)
    Права - владелец нотифа или админ.
    '''
    serializer_class = NotifSerializer
    queryset = Notif.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticated3,)

class NotifIsReadOrStatus4(generics.ListAPIView):
    '''
    Представление для изменения свойства is_read или 
    выставления status в 4.
    pk1 - user id
    pk2 - notif id
    pk3 - 0/1 (is_read/status)
    Права - нет.
    '''
    serializer_class = NotifSerializer
    queryset = Notif.objects.all()
    permission_classes = (CustomIsAuthenticated4,)

    def get_queryset(self):
        n = Notif.objects.get(id=self.kwargs['pk2'])
        if self.kwargs['pk3'] == "0":
            u = User.objects.get(id=self.kwargs['pk1'])
            n.is_read.add(u)
        if self.kwargs['pk3'] == "1":
            n.status = 4
        n.save()
        return Notif.objects.filter(id=self.kwargs['pk2'])

class UserFromTokenViewSet(viewsets.ModelViewSet):
    '''
    Получить id по токену.
    Права - нет.
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
    Права - админ.
    '''
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    def send_the_mail(self, request):
        email = request.data['email']
        if request.data['is_staff'] == 'true': is_staff = True
        else: is_staff = False
        print(is_staff)
        photo = request.data['photo']
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

        user = User.objects.create_user(
            email = email,
            password = password,
            username = email,
            is_staff = is_staff
        )
        uP = UserProfile.objects.filter(user_id=user.id)
        uP.update(
            second_name = email,
            position = "Должность не указана",
        )
        uP1 = UserProfile.objects.get(user_id=user.id)

        print(type(photo))
        print(photo)

        import base64
        format, imgstr = photo.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        uP1.photo.save('new_file_name', data)

        uP1.save()
        user.save()
        
        send_mail(
            'Приглашение от СЭД МТУСИ',
            message_text,
            'edmsmtuci@gmail.com',
            [email,],
            fail_silently=False,
        )

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
