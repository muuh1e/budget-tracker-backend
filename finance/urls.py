# finance/urls.py
from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, TransactionViewSet, DashboardViewSet

app_name = "finance"

router = routers.DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"transactions", TransactionViewSet, basename="transaction")
router.register(r"dashboard", DashboardViewSet, basename="dashboard")

urlpatterns = [
    # /api/categories/, /api/transactions/, /api/dashboard/
    path("", include(router.urls)),
]
