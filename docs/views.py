from rest_framework.response import Response
from .serializers import (
    DocSerializer,
)
from users.serializers import (
    UserSerializer,
    NotifSerializer
)
from users.models import Notif
from .permissions import CustomIsAuthenticated
from .models import Doc
from rest_framework import (
    generics,
    mixins,
    viewsets,
    permissions,
    views
)
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
        print(request.data)
        notif = Notif.objects.create(
            user_id=request.data["user_id"], 
            doc_id=serializer.data["id"],
            is_owner=True,
            is_signature_request=False)
        return Response(serializer.data)
