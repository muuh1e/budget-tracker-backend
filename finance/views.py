# transactions/views.py

from rest_framework import viewsets, filters, mixins, status
from django_filters.rest_framework import DjangoFilterBackend               
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from .models import Category, Transaction
from .serializers import (
    CategorySerializer,
    TransactionSerializer,
    DashboardSummarySerializer,
)
from .permissions import IsOwner
from .services import financial_summary
from .filters import TransactionFilter

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




class DashboardViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    GET /dashboard/   →  {'total_income': …, 'total_expense': …, 'balance': …}
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DashboardSummarySerializer   # just for schema

    def list(self, request, *args, **kwargs):
        data = financial_summary(user=request.user)          # ← single call
        return Response(data)
    


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

# class CategoryViewSet(viewsets.ModelViewSet):
#     """
#     Create / list / edit / delete categories (only user-owned)
#     """
#     serializer_class = CategorySerializer
#     permission_classes = [IsAuthenticated, IsOwner]
#     pagination_class = None  # usually small enough to not paginate

#     def get_queryset(self):
#         return Category.objects.filter(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Create / list / edit / delete categories (only user-owned)
    """
    serializer_class   = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class   = None  # usually small enough to not paginate

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="List Categories",
        operation_description="Retrieve all categories for the authenticated user.",
        responses={
            200: openapi.Response(
                description="A list of categories",
                schema=CategorySerializer(many=True),
                examples={
                    "application/json": [
                        {"id": 1, "name": "Groceries", "user": 3},
                        {"id": 2, "name": "Rent",      "user": 3},
                    ]
                }
            )
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Category",
        operation_description="Create a new category. Name must be unique per user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Category title',
                    example='Groceries'
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Category created",
                schema=CategorySerializer,
                examples={
                    "application/json": {"id": 7, "name": "Groceries", "user": 3}
                }
            ),
            400: "Validation errors"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Category",
        operation_description="Get details of a specific category by its ID.",
        responses={200: CategorySerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Category",
        operation_description="Rename an existing category you own.",
        request_body=CategorySerializer,
        responses={200: CategorySerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Category",
        operation_description="Remove a category. Transactions in this category will not be deleted.",
        responses={204: "No content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
class TransactionViewSet(viewsets.ModelViewSet):
    """
    CRUD transactions with pagination and optional filtering
    by date or category:contentReference[oaicite:2]{index=2}.
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TransactionFilter
    ordering_fields = ['date', 'amount', 'type']
    
    ## Custom actions for aggregating data, implemented before using DjangoFilterBackend
    @action(detail=False, url_path='by-category')
    def by_category(self, request):
        qs = Transaction.objects.filter(category__user=request.user)
        grouped = (
            qs
            .values('category', 'category__name')
            .annotate(total_amount=Sum('amount'), txn_count=Count('id'))
            .order_by('category__name')
        )
        return Response(grouped)

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        
        # Start with a filtered queryset based on the logged-in user's categories
        queryset = Transaction.objects.filter(category__user=self.request.user)
        
        if category_id:
            # If category_id is provided, filter by that category as well
            queryset = queryset.filter(category__id=category_id)
        
        # Eagerly load related categories to avoid N+1 queries
        return queryset.select_related('category')
    
    
    ## Override get_serializer_context to pre-fetch user categories and pass them to the serializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Only pre-fetch categories for write operations (POST/PUT/PATCH)
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            user_categories = Category.objects.filter(user=self.request.user).only('id', 'name')
            context['user_categories'] = user_categories
        return context



