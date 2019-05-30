from rest_framework import permissions
from .models import Doc
from users.models import Notif

class CustomIsAuthenticated(permissions.BasePermission):        
    '''
    + POST - аутентификация и админ
    + GET все юзеры - пусто
    + GET один пользователь - аутентификация и (владелец нотифа или админ)
    '''
    def has_permission(self, request, view):
        if request.method == 'GET':
            notif = Notif.objects.get(
                doc_id=view.kwargs['pk'],
                status=2
            )
            return request.user.is_authenticated and (notif.user.id == request.user.id or request.user.is_staff)
        return request.user and request.user.is_authenticated
