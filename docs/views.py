from PIL import Image
from rest_framework import status
import boto3
import os
from django.core import exceptions
from rest_framework.response import Response
from .serializers import (
    DocSerializer,
    FileCabinetSerializer
)
from users.serializers import (
    UserSerializer,
    NotifSerializer
)
from users.models import (
    Notif,
    User
)
from .permissions import (
    CustomIsAuthenticated,
    CustomIsAuthenticated2,
    CustomIsAuthenticated3,
    CustomIsAuthenticated4,
)
from .models import (
    Doc,
    FileCabinet
)
from rest_framework import (
    generics,
    mixins,
    viewsets,
    permissions,
    views
)
from edc.EDC import EDC
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
import datetime

class DocViewSet(viewsets.ModelViewSet):
    '''
    Универсальное представление для работы с документами.
    При создании документа обязательно указывать user_id, потому 
    что создается еще запись Notif, где есть созданный документ и 
    указанный пользователь в user_id.
    Права - админ или владелец.
    '''
    serializer_class = DocSerializer
    queryset = Doc.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticated,)

    def list(self, request):
        queryset = Doc.objects.filter(common=True)
        serializer = DocSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            now = datetime.datetime.now()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            notif = Notif.objects.create(
                user_id=request.data["user_id"], 
                doc_id=serializer.data["id"],
                status=0,
                date=now.strftime("%Y-%m-%d")
            )
            serializerNotif = NotifSerializer(notif)
            return Response(serializerNotif.data)
        except Exception as e:
            raise exceptions.ValidationError(str(e))


class FileCabinetViewSet(viewsets.ModelViewSet):
    '''
    Универсальное представление для работы с картотеками.
    '''
    serializer_class = FileCabinetSerializer
    queryset = FileCabinet.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticated4,)

class AddSignature(generics.ListAPIView):
    '''
    Добавить подпись к документу. Принимает id документа.
    Права - нет (они проверяются на сервере генерации подписи).
    '''
    serializer_class = DocSerializer
    queryset = Doc.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticated2,)

    def get_queryset(self):
        # Найти нужный документ
        doc = Doc.objects.get(id=self.kwargs['pk'])

        # Найти нотиф, который с этим документом и
        # пользователь - владелец документа
        notifOwner = Notif.objects.get(
            doc_id=doc.id,
            status=0
        )

        # Тут должна быть функция генерации подписи
        edc = EDC()
        if self.kwargs['first'] == '0':
            path = 'https://edms-mtuci.s3.amazonaws.com/' + str(doc.file)
        elif self.kwargs['first'] == '1':
            print('Первая подпись')
            path = 'https://edms-mtuci.s3.amazonaws.com/' + str(doc.file)

        try:
            s3 = boto3.resource(
                's3',
                aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            )
            s3.meta.client.download_file(
                'edms-mtuci',
                'media/'+str(doc.file),
                'staticfiles/media/'+str(doc.file)
            )
        except: pass

        file = open('staticfiles/media/' + str(doc.file), 'rb')
        signature = edc.signFile(file, notifOwner.user.username)

        # print('fo0', str(doc.file))
        # first_object = s3.Object('edms-mtuci', str(doc.file))
        # print('fo', first_object)

        # import base64
        # # f = open(signature, 'r').read()
        # c = base64.b64decode(signature)
        # print(c)

        # Добавить подпись
        doc.signature = signature
        doc.save()

        # Подпись ставит не владелец
        if self.kwargs['first'] == '0':
            # Найти нотиф, который с этим документом и
            # где очередь подписывать и изменить на "подписано"
            try:
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
            except Exception as e:
                pass
        doc = Doc.objects.filter(id=self.kwargs['pk'])
        serializer = DocSerializer(doc)
        return doc

class DownloadFile(generics.RetrieveAPIView):
    '''
    Скачать файл.
    Права - нет (они проверяются на сервере генерации подписи).
    '''
    serializer_class = DocSerializer
    queryset = Doc.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticated3,)

    def get(self, request, pk):
        doc = Doc.objects.get(id=self.kwargs['pk'])
        s3 = boto3.resource(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        )
        print(str(doc.file))
        s3.meta.client.download_file(
            'edms-mtuci', 
            'media/'+str(doc.file), 
            'staticfiles/media/'+str(doc.file)
        )
        print(str(doc.file))
        return Response({'file': 'media/'+str(doc.file)})
