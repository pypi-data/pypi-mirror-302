from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView

from src.account.urls import (
    invitations_router,
    password_router,
    permission_router,
    roles_router,
    user_router,
)
from src.account.views.token import CustomTokenRefreshView
from src.common.urls import organisation_router, profiles_router

v1_urls = [
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("user/", include(user_router.urls)),
    path("invitation/", include(invitations_router.urls)),
    path("profiles/", include(profiles_router.urls)),
    path("organisations/", include(organisation_router.urls)),
    path("password/", include(password_router.urls)),
    path("roles/", include(roles_router.urls)),
    path("permissions/", include(permission_router.urls)),
]


urlpatterns = [
    path("api/v1/", include((v1_urls, "v1"), namespace="v1")),
    path("admin/", admin.site.urls),
    # API docs UI:
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
