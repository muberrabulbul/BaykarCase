"""
Baykar IHA Rental URL Configuration
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from baykaraccounts import views as accounts_views
from category import views as category_views
from rental import views as rentals_views
from ihas import views as ihas_views
from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Baykar IHA Rental REST API",
        default_version="v1",
        description="Documentation on Baykar IHA Rental REST API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r"categories", category_views.CategoryViewSet)
router.register(r"ihas", ihas_views.IHAViewSet)
router.register(r"iha-photos", ihas_views.IHAPhotoViewSet)
router.register(r"users", accounts_views.UserViewSet, basename="users")

router.register(r"rentals", rentals_views.RentalViewSet, basename="rentals")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("register/", accounts_views.RegisterAPIView.as_view(), name="register"),
    path("login/", accounts_views.CustomLoginView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "swagger-doc/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api-auth/", include("rest_framework.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
