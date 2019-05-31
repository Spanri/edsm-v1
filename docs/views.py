from PIL import Image
from rest_framework import status
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
from users.models import Notif
from .permissions import CustomIsAuthenticated
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

class DocViewSet(viewsets.ModelViewSet):
    '''
    При создании документа обязательно указывать user_id, потому 
    что создается еще запись Notif, где есть созданный документ и 
    указанный пользователь в user_id.
    '''
    serializer_class = DocSerializer
    queryset = Doc.objects.all()
    permission_classes = ()

    def list(self, request):
        queryset = Doc.objects.filter(common=True)
        serializer = DocSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        try:
            notif = Notif.objects.create(
                user_id=request.data["user_id"], 
                doc_id=serializer.data["id"],
                status=0,
            )
        except Exception as e:
            raise exceptions.ValidationError(str(e))
        return Response(serializer.data)


class FileCabinetViewSet(viewsets.ModelViewSet):
    '''
    Универсальное представление для работы с картотеками.
    '''
    serializer_class = FileCabinetSerializer
    queryset = FileCabinet.objects.all()
    permission_classes = ()

class AddSignature(generics.ListAPIView):
    '''
    Добавить подпись к документу. Принимает id документа.
    Права - нет (они проверяются на сервере генерации подписи).
    '''
    serializer_class = DocSerializer
    queryset = Doc.objects.all()
    permission_classes = ()

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
        path = doc.file
        path = "edc/test.txt"
        file = open(str(path), "r")
        signature = edc.signFile(file, notifOwner.user.username)

        # Добавить подпись
        doc.signature = signature
        doc.save()

        # Найти нотиф, который с этим документом и
        # где очередь подписывать и изменить на "подписано"
        try:
            notif = Notif.objects.get(
                doc_id=doc.id,
                status=2
            )
            notif.status = 3
            notif.save()
        except Exception as e:
            raise exceptions.ValidationError(str(e))

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
        
        doc = Doc.objects.filter(id=self.kwargs['pk'])
        serializer = DocSerializer(doc)
        return doc
