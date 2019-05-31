from rest_framework import permissions
from .models import User

class CustomIsAuthenticated(permissions.BasePermission):        
    '''
    + POST - админ
    + GET все юзеры - пусто
    + GET один пользователь - админ или (аутентификация и владелец)
    '''
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        # if request.method == 'GET':
        #     return request.user.is_staff
        if request.method == 'PUT':
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (obj.id == request.user.id)


class CustomIsAuthenticated2(permissions.BasePermission):
    '''
    Для всех нотифов пользователя, админ или (аутентификация и владелец).
    '''
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user and request.user.is_authenticated and int(view.kwargs['pk']) == request.user.id
