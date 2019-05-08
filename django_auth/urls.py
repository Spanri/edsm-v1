from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from users.views import (
    UserViewSet, 
    SendInviteView,
    ObtainAuthToken,
    UserFromTokenViewSet,
    Index,
    ConfirmUpdatePasswordView,
)

from rest_framework import routers
router = routers.DefaultRouter(trailing_slash = False)
router.register(r'^api/users', UserViewSet)
urlpatterns = router.urls

urlpatterns += [
    url(r'^api/send_invite/$', SendInviteView.as_view({"post": "send_the_mail"})),
    url(r'^api/confirm_update_password/$', ConfirmUpdatePasswordView.as_view({"post": "confirm_update_password"})),
    url(r'^api/get_auth_token/$', ObtainAuthToken.as_view()),
    url(r'^api/get_user_from_token/$', UserFromTokenViewSet.as_view({'get': 'list'})),
    url(r'^api/admin/', admin.site.urls), # Для разработчика
    url(r'^index/', Index.as_view()),
    # url(r'', TemplateView.as_view(template_name='public/index.html'),  name='Home')
]

urlpatterns.append(
    url(r'^docs/', include_docs_urls(
            title='СЭД МТУСИ',
            permission_classes=(),
            patterns=urlpatterns
        )
    )
)

# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
