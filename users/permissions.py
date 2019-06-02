from rest_framework import permissions
from .models import User, Notif

class CustomIsAuthenticated(permissions.BasePermission):        
    '''
    Для работы с пользователями.
    + POST - все
    + GET все - админ
    + GET один, PUT, PATCH, DELETE - админ или владелец
    '''
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        if (
            view.action == 'retrieve' or 
            request.method in ['POST', 'PUT', 'PATCH', 'DELETE']
        ):
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return request.user.is_authenticated and obj.id == request.user.id
        
class CustomIsAuthenticated2(permissions.BasePermission):
    '''
    Для всех нотифов пользователя, админ или владелец.
    '''
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user and request.user.is_authenticated and int(view.kwargs['pk']) == request.user.id

class CustomIsAuthenticated3(permissions.BasePermission):
    '''
    Для работы с нотифами.
    + POST - все
    + GET все - админ
    + GET один, PUT, PATCH, DELETE - админ или владелец
    '''
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        if (
            view.action == 'retrieve' or
            request.method in ['PUT', 'PATCH', 'DELETE']
        ):
            return True
        if request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        notif = Notif.objects.get(id=view.kwargs['pk'])
        return request.user.is_authenticated and notif.user.id == request.user.id

class CustomIsAuthenticated4(permissions.BasePermission):
    '''
    Для добавления к документу пользователя как юзера, который 
    прочитал этот документ (в поле is_read). Админ или владелец.
    '''
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user and request.user.is_authenticated and int(view.kwargs['pk1']) == request.user.id
