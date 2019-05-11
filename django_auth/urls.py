from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from django.conf.urls.static import static
from django.conf import settings
from users.views import (
    UserViewSet, 
    SendInviteView,
    ObtainAuthToken,
    UserFromTokenViewSet,
    Index,
    ConfirmUpdatePasswordView,
    GetAllEmails,
)

# Создание пользователей, получение всего списка, получение 
# одного пользователя, patch, put
from rest_framework import routers
router = routers.DefaultRouter(trailing_slash = False)
router.register(r'^users', UserViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', Index.as_view()),
    url(r'^api/all_emails/$', GetAllEmails.as_view()),
    url(r'^api/send_invite/$', SendInviteView.as_view({'post': 'send_the_mail'})),
]

# Работа с токенами
urlpatterns += [
    url(r'^api/get_auth_token/$', ObtainAuthToken.as_view()),
    url(r'^api/get_user_from_token/$', UserFromTokenViewSet.as_view({'get': 'list'})),
]

# Для сброса пароля
urlpatterns += [
    url(r'^rest_auth/', include('rest_auth.urls')),
]

# Для файлов
urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

# Для разработчика
urlpatterns += [
    url(r'^api/admin/', admin.site.urls),
]

# Документация
urlpatterns += [
    url(r'^docs/', include_docs_urls(
            title='СЭД МТУСИ',
            permission_classes=(),
            patterns=urlpatterns
        )
    )
]
