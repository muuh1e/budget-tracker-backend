# finance/services.py
from decimal import Decimal
from django.db.models import Sum, Case, When, F, DecimalField

from finance.models import Transaction


def financial_summary(*, user, start=None, end=None):
    """
    Return {'total_income', 'total_expense', 'balance'} for ``user``.
    Pass optional ``start`` / ``end`` dates to limit the range.
    """

    qs = Transaction.objects.filter(category__user=user)

    if start:
        qs = qs.filter(date__gte=start)
    if end:
        qs = qs.filter(date__lte=end)

    sums = qs.aggregate(
        income=Sum(
            Case(
                When(type=Transaction.TransactionType.INCOME, then=F("amount")),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        ),
        expense=Sum(
            Case(
                When(type=Transaction.TransactionType.EXPENSE, then=F("amount")),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        ),
    )

    income  = sums["income"]  or Decimal("0")
    expense = sums["expense"] or Decimal("0")
    return {
        "total_income":  income,
        "total_expense": expense,
        "balance":       income - expense,
    }
