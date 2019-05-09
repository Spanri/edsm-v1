from django.conf.urls import url, include
from django.contrib import admin
# from django.contrib.auth import views as viewsR
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

# Создание пользователей, получение всего списка, получение 
# одного пользователя, patch, put
from rest_framework import routers
router = routers.DefaultRouter(trailing_slash = False)
router.register(r'^api/users', UserViewSet)
urlpatterns = router.urls

urlpatterns += [
    url(r'^api/send_invite/$', SendInviteView.as_view({"post": "send_the_mail"})),
    url(r'^api/confirm_update_password/$', ConfirmUpdatePasswordView.as_view({"post": "confirm_update_password"})),
    url(r'^index/', Index.as_view()),
    # url(r'', TemplateView.as_view(template_name='public/index.html'),  name='Home')
]

# Работа с токенами
urlpatterns += [
    url(r'^api/get_auth_token/$', ObtainAuthToken.as_view()),
    url(r'^api/get_user_from_token/$', UserFromTokenViewSet.as_view({'get': 'list'})),
]

# Для сброса пароля
urlpatterns += [
    url(r'^rest-auth/', include('rest_auth.urls')),
    # для генерации в email ссылки сброса пароля
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$', 
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'
    ),
]

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

# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
