from rest_framework import permissions
from .models import Doc

class CustomIsAuthenticated(permissions.BasePermission):        
    '''
    + POST - аутентификация и админ
    + GET все юзеры - пусто
    + GET один пользователь - аутентификация и владелец
    '''
    def has_permission(self, request, view):
        if request.method == 'GET' or request.method == 'PUT':
            return True
        return request.user and request.user.is_authenticated or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (obj.id == request.user.id or request.user.is_staff)