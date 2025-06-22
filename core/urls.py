# core/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserRegisterView, LogoutView

app_name = "core"

urlpatterns = [
    # POST /api/auth/register/
    path("register/", UserRegisterView.as_view(), name="user-register"),
    # POST /api/auth/token/      → { access, refresh }
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # POST /api/auth/token/refresh/
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # POST /api/auth/logout/
    path("logout/", LogoutView.as_view(), name="logout"),
]
