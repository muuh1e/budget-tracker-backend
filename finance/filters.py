# transactions/filters.py

import django_filters
from .models import Transaction, Category

class TransactionFilter(django_filters.FilterSet):
    # Date range
    date_after = django_filters.DateFilter(
        field_name='date', lookup_expr='gte', label='Date from'
    )
    date_before = django_filters.DateFilter(
        field_name='date', lookup_expr='lte', label='Date to'
    )

    # Amount range
    amount_min = django_filters.NumberFilter(
        field_name='amount', lookup_expr='gte', label='Min amount'
    )
    amount_max = django_filters.NumberFilter(
        field_name='amount', lookup_expr='lte', label='Max amount'
    )

    # Transaction type via TextChoices
    type = django_filters.ChoiceFilter(
        field_name='type',
        choices=Transaction.TransactionType.choices,
        label='Transaction type'
    )

    # Category is declared up-front with no choices
    category = django_filters.ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.none(),
        label='Category'
    )
    category_name = django_filters.CharFilter(
        field_name='category__name',
        lookup_expr='icontains',
        label='Category name contains'
    )

    # Text search on `note`
    note = django_filters.CharFilter(
        field_name='note',
        lookup_expr='icontains',
        label='Note contains'
    )

    class Meta:
        model = Transaction
        fields = [
            'date_after', 'date_before',
            'amount_min', 'amount_max',
            'type',
            'category', 'category_name',
            'note',
        ]

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        """
        Override __init__ to inject only this user's categories into the
        `category` filter's queryset. DjangoFilterBackend will pass
        `request=` when it instantiates this FilterSet.
        """
        super().__init__(data=data, queryset=queryset, request=request, prefix=prefix)
        user = getattr(request, 'user', None)
        if user and not user.is_anonymous:
            self.filters['category'].queryset = Category.objects.filter(user=user)
