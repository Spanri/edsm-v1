from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from django.conf.urls.static import static
from django.conf import settings
from users.views import (
    UserViewSet, 
    NotifViewSet, 
    SendInviteView,
    ObtainAuthToken,
    UserFromTokenViewSet,
    Index,
    ConfirmUpdatePasswordView,
    AddSignature,
    Notif2,
    # GetEmail,
    # DocsOwner,
    # AllDocs,
    # Notif1,
    # DocsOwnerOne,
)
from docs.views import (
    DocViewSet,
)

# Создание пользователей, получение всего списка, получение 
# одного пользователя, patch, put
from rest_framework import routers
router = routers.DefaultRouter(trailing_slash = False)
router.register(r'^users/i', UserViewSet)
router.register(r'^users/notif', NotifViewSet)
router.register(r'^docs', DocViewSet)
# router.register(r'^docs2', DocViewSet2)

urlpatterns = [
    # url(r'^api/users/(?P<pk>.+)/docs/$', DocsOwner.as_view()),
    # url(r'^api/users/docs/(?P<pk>.+)/$', DocsOwnerOne.as_view()),
    # url(r'^api/users/all_docs/$', AllDocs.as_view()),
    # url(r'^api/users/notif/common/$', Notif1.as_view()),
    url(r'^api/users/(?P<pk>.+)/notif/$', Notif2.as_view()),
    url(r'^api/users/notif/add_signature/$',
        AddSignature.as_view({'post': 'add_signature'})),
    url(r'^api/', include(router.urls)),
    # url(r'^api/users/email/(?P<pk>.+)/$', GetEmail.as_view()),
    url(r'^api/users/send_invite/$', SendInviteView.as_view({'post': 'send_the_mail'})),
]

# Работа с токенами
urlpatterns += [
    url(r'^api/users/get_auth_token/$', ObtainAuthToken.as_view()),
    url(r'^api/users/get_user_from_token/$', UserFromTokenViewSet.as_view({'get': 'list'})),
]

# Для сброса пароля
urlpatterns += [
    url(r'^api/users/rest_auth/', include('rest_auth.urls')),
]

# Документы
urlpatterns += [
    
]

# Для разработчика
urlpatterns += [
    url(r'^api/admin/', admin.site.urls),
]

# Документация
urlpatterns += [
    url(r'^api/docsServer/', include_docs_urls(
            title='СЭД МТУСИ',
            permission_classes=(),
            patterns=urlpatterns
        )
    )
]

urlpatterns += [
    url(r'^app/*', Index.as_view(), name='index'),
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
