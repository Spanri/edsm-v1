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
import copy

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
    '''
    serializer_class = NotifSerializer
    queryset = Notif.objects.all()
    permission_classes = ()

    def list(self, request, *args, **kwargs):
        notif = super(Notif2, self).list(request, args, kwargs)
        notif2 = []
        notif_owner = []
        notif_common = []
        user_id = int(self.kwargs['pk'])
        for i, n in enumerate(notif.data):
            d = {}
            for idx, val in enumerate(n):
                d.setdefault(val, n[val])
            notif.data[i] = d
            # надо подписать и очередь или
            # подписан и есть уведомления или
            # просто смотрю, не надо подписывать
            if(
                n['user']['id'] == user_id and
                (
                    n['status'] == 2 or
                    n['status'] == 3 or
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
                n['status'] == 0
            ):
                notif2.append(notif.data[i])
        notif2 = notif2 + notif_owner
        # Находим документы пользователя, которые подписали, чтобы
        # вывести это в уведомления с сообщением "Ваш документ подписали."
        # Для каждого документа, где пользователь - владелец, проверяем,
        # есть ли нотиф, где этот документ и
        # is_owner=false, is_signature_request=true, is_signature=true
        notif_signature = []
        for i, n in enumerate(notif_owner):
            for j, n2 in enumerate(notif.data):
                if(
                    n2['doc']['id'] == n['doc']['id'] and
                    n2['status'] == 3
                ):
                    notif_signature.append(n2)
                    break
        notif2 = notif2 + notif_signature
        # Если подписал сам владелец, то пусть будет
        # статус = 6 (в таблице оригинальной он нигде не занят)
        for i, n in enumerate(notif2):
            for j, n2 in enumerate(notif2):
                if(
                    n2['user']['id'] == user_id and
                    (n2['status'] == 3 or n2['status'] == 4)
                ):
                    notif2[j]['status'] = 6
                    break
        notif3 = copy.deepcopy(notif.data)
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
        return Response(notif2)

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
            status=2
        )
        notif.status = 3
        notif.save()

        # Найти следующий нотиф, который с этим документом и
        # где очередь = очередь+1
        try:
            notifNext = Notif.objects.get(
                doc_id=doc.id,
                status=1,
                queue=notif.queue+1
            )
            notifNext.status = 2
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
