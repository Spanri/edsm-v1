from rest_framework.response import Response
from .serializers import (
    DocSerializer,
)
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
    Универсальное представление для работы с документами.
    '''
    serializer_class = DocSerializer
    queryset = Doc.objects.all()
    permission_classes = ()
