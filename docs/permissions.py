from rest_framework import permissions
from .models import Doc
from users.models import Notif

class CustomIsAuthenticated(permissions.BasePermission):        
    '''
    Для работы с документами.
    + POST - все
    + GET все - админ
    + GET один (статус=0), PUT, PATCH, DELETE - админ или владелец
    '''
    def has_permission(self, request, view):
        if request.user.is_staff or request.method == 'POST':
            return True
        if view.action == 'retrieve':
            doc = Doc.objects.get(id=view.kwargs['pk'])
            if doc.common:
                return True
            notif = Notif.objects.filter(doc_id=view.kwargs['pk'])
            r = False
            for n in notif:
                r = n.user.id == request.user.id
                if r:
                    break
            return request.user.is_authenticated and r
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            try:
                notif1 = Notif.objects.get(
                    doc_id=view.kwargs['pk'],
                    status=0
                )
                return request.user.is_authenticated and notif1.user.id == request.user.id
            except: pass
        return request.user and request.user.is_authenticated and request.user.is_staff
class CustomIsAuthenticated2(permissions.BasePermission):
    '''
    Для добавления подписи, админ или владелец нотифа, который с этим 
    документом и который надо подписать.
    '''
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        try:
            notif1 = Notif.objects.get(
                doc_id=view.kwargs['pk'],
                status=2
            )
            return request.user.is_authenticated and notif1.user.id == request.user.id
        except: pass
        return request.user and request.user.is_authenticated and request.user.is_staff

class CustomIsAuthenticated3(permissions.BasePermission):
    '''
    Для скачивания документа. Права у админа или владельца нотифа с этим документом 
    (любой статус), у всех, если документ в общем доступе.
    '''
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        doc = Doc.objects.get(id=view.kwargs['pk'])
        if doc.common: return True
        notif = Notif.objects.filter(doc_id=view.kwargs['pk'])
        r = False
        for n in notif:
            r = n.user.id == request.user.id
            if r: break
        return request.user.is_authenticated and r

class CustomIsAuthenticated4(permissions.BasePermission):
    '''
    Для работы с картотеками.
    + GET все, один - все
    + POST, PUT, PATCH, DELETE - админ
    '''
    def has_permission(self, request, view):
        return view.action == 'retrieve' or request.method == 'GET' or request.user.is_staff
