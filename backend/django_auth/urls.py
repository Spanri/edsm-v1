from django.conf.urls import url, include
from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

from django.contrib import admin
from users.views import UserViewSet, SendInviteView, UserUpdateView

from rest_framework import routers
router = routers.DefaultRouter(trailing_slash = False)
router.register(r'^users', UserViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(r'^update/user/(?P<pk>\d+)/', UserUpdateView.as_view(), name='user_update'),
    url(r'send_invite/$', SendInviteView.as_view({"post": "send_the_mail"})),
    # url(r'^user/$', Login.as_view({'get': 'login'}), name='user-login'),
    # auth-jwt принимает email и password, возвращается token
    url(r'^auth/jwt/', obtain_jwt_token),
    url(r'^auth/jwt-refresh/', refresh_jwt_token),
    # auth-jwt-verify принимает токен и возвращает токен
    url(r'^auth/jwt-verify/', verify_jwt_token),
    # Для разработчика
    url(r'^admin/', admin.site.urls),
]
