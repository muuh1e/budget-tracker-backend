# PhotoCart/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# --- Swagger / OpenAPI setup ---
schema_view = get_schema_view(
    openapi.Info(
        title="PhotoCart API",
        default_version="v1",
        description="API documentation for the PhotoCart application",
        contact=openapi.Contact(
            name="PhotoCart Support",
            email="medx11e@gmail.com",
            url="https://photocart.example.com/help/"
        ),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

swagger_patterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui"
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc"
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls),

    # Authentication
    path("api/auth/", include("core.urls", namespace="core")),

    # Finance domain endpoints
    path("api/", include("finance.urls", namespace="finance")),

    # Browsable-API login/logout
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),

    # Django Debug Toolbar
    path("__debug__/", include("debug_toolbar.urls")),
] + swagger_patterns
