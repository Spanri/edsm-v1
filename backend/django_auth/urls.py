from django.conf.urls import url, include
from django.urls import path

from django.contrib import admin
from users.views import UserViewSet, SendInviteView, UserUpdateView

from rest_framework import routers
router = routers.DefaultRouter(trailing_slash = False)
router.register(r'^users', UserViewSet)

from rest_framework.authtoken import views as rviews

urlpatterns = router.urls

urlpatterns += [
    url(r'^update_user/(?P<pk>\d+)/', UserUpdateView.as_view(), name='user_update'),
    url(r'^send_invite/$', SendInviteView.as_view({"post": "send_the_mail"})),
    # url(r'^user/$', Login.as_view({'get': 'login'}), name='user-login'),
    # принимает email и password, возвращает token
    url(r'^get_auth_token/$', rviews.obtain_auth_token),
    # Для разработчика
    url(r'^admin/', admin.site.urls),
]
