from rest_framework.response import Response
from .serializers import (
    DocSerializer,
)
from users.serializers import (
    UserSerializer,
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
    Возвращает список только из тех документов, которые в общем доступе.
    '''
    serializer_class = DocSerializer
    queryset = Doc.objects.all()
    permission_classes = ()

    def list(self, request):
        queryset = Doc.objects.filter(common=True)
        serializer = DocSerializer(queryset, many=True)
        return Response(serializer.data)