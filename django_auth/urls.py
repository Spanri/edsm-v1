from django.conf.urls import url, include
from django.urls import include, re_path
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView
from users.views import (
    UserViewSet, 
    NotifViewSet, 
    SendInviteView,
    ObtainAuthToken,
    UserFromTokenViewSet,
    Index,
    ConfirmUpdatePasswordView,
    Notif2,
    NotifQueue,
    NotifIsReadOrStatus4,
    GetEmails,
    UserPhoto
)
from docs.views import (
    DocViewSet,
    FileCabinetViewSet,
    AddSignature,
    CancelSignature,
    SignatureAgain,
    DownloadFile,
    DownloadSign,
    DeleteFileFromLocal
)

# Создание пользователей, получение всего списка, получение 
# одного пользователя, patch, put
from rest_framework import routers
router = routers.DefaultRouter(trailing_slash = False)
router.register(r'^users/i', UserViewSet)
router.register(r'^users/notif', NotifViewSet)
router.register(r'^docs/i', DocViewSet)
router.register(r'^docs/fileCabinets', FileCabinetViewSet)
# router.register(r'^docs2', DocViewSet2)

urlpatterns = [
    url(r'^api/users/(?P<pk>.+)/photo/$', UserPhoto),
    url(r'^api/users/(?P<pk>.+)/notif/$', Notif2.as_view()),
    url(r'^api/users/(?P<pk1>.+)/notif/(?P<pk2>.+)/(?P<pk3>.+)/$',
        NotifIsReadOrStatus4.as_view()),
    url(r'^api/docs/add_signature/(?P<pk>.+)/(?P<first>.+)/$', AddSignature.as_view()),
    url(r'^api/docs/cancel_signature/(?P<pk>.+)/$',
        CancelSignature.as_view({'post': 'cancel_signature'})),
    url(r'^api/docs/signature_again/(?P<pk>.+)/$', SignatureAgain.as_view()),
    url(r'^api/docs/signature_queue/(?P<pk>.+)/$', NotifQueue.as_view()),
    url(r'^api/docs/download/(?P<pk>.+)/$', DownloadFile.as_view()),
    url(r'^api/docs/download_sign/(?P<pk>.+)/$', DownloadSign.as_view()),
    url(r'^api/docs/delete_from_local/(?P<pk>.+)/(?P<type>.+)/$', DeleteFileFromLocal.as_view()),
    url(r'^api/', include(router.urls)),
    url(r'^api/users/emails/$', GetEmails.as_view()),
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

favicon_view = RedirectView.as_view(url='/favicon.ico', permanent=True)

urlpatterns += [
    url(r'^$', RedirectView.as_view(url='/app')),
    url(r'^app/*', Index.as_view(), name='index'),
    re_path(r'^favicon\.ico$', favicon_view),
]

# Для файлов
urlpatterns += static(settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
