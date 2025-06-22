# photocart/core/tasks.py
import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta, date
from django.db.models import Sum
from decimal import Decimal # <--- IMPORT THIS

from django.contrib.auth import get_user_model
from finance.models import Transaction, Category

logger = logging.getLogger(__name__)

User = get_user_model()

@shared_task
def debug_task(name="World"):
    """
    A simple Celery task to demonstrate functionality.
    """
    message = f"Hello, {name}! This is a debug task running at {debug_task.request.hostname}"
    logger.info(message)
    print(message)
    return message

@shared_task
def send_user_summary_report(user_id, period="weekly"):
    """
    Celery task to send a user's financial summary report via email.

    Args:
        user_id (int): The ID of the user for whom to generate the report.
        period (str): The reporting period ('weekly' or 'monthly').
    """
    try:
        user = User.objects.get(id=user_id)
        user_email = user.email
    except User.DoesNotExist:
        logger.error(f"send_user_summary_report: User with ID {user_id} not found. Skipping email report.")
        return

    subject = f"Your {period.capitalize()} Financial Summary Report - PhotoCart"
    to_email = [user_email]

    end_date = date.today()
    start_date = None

    if period == "weekly":
        start_date = end_date - timedelta(days=7)
    elif period == "monthly":
        start_date = end_date - timedelta(days=30)
    else:
        logger.warning(f"send_user_summary_report: Unknown period '{period}' for user {user_id}. No report generated.")
        return

    transactions_in_period = Transaction.objects.filter(
        category__user=user,
        date__range=[start_date, end_date]
    )

    # Ensure fallbacks are Decimal objects
    total_income = transactions_in_period.filter(
        type=Transaction.TransactionType.INCOME
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00') # <--- CHANGED HERE
    
    total_expense = transactions_in_period.filter(
        type=Transaction.TransactionType.EXPENSE
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00') # <--- CHANGED HERE

    net_balance_change = total_income - total_expense

    email_body = f"""
Dear {user.first_name if user.first_name else user.email},

Here is your {period} financial summary for the period from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}:

---------------------------------------------------
Total Income: ${total_income:.2f}
Total Expenses: ${total_expense:.2f}
Net Balance Change (Income - Expenses): ${net_balance_change:.2f}
---------------------------------------------------

"""
    recent_transactions = transactions_in_period.order_by('-date')[:5]
    if recent_transactions.exists():
        email_body += "\nRecent Transactions:\n"
        for trans in recent_transactions:
            category_name = trans.category.name if trans.category else "Uncategorized"
            email_body += f"- {trans.get_type_display()}: ${trans.amount:.2f} on {trans.date.strftime('%Y-%m-%d')} ({category_name}) - {trans.note if trans.note else 'No note'}\n"
    else:
        email_body += "\nNo transactions recorded for this period."

    email_body += """

Thank you for using PhotoCart!

Best regards,
The PhotoCart Team
"""

    try:
        send_mail(
            subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            to_email,
            fail_silently=False,
        )
        logger.info(f"send_user_summary_report: Successfully sent {period} summary report to {user_email}")
        print(f"Successfully sent {period} summary report to {user_email}")
    except Exception as e:
        logger.error(f"send_user_summary_report: Failed to send {period} summary report to {user_email}: {e}")
        print(f"Failed to send {period} summary report to {user_email}: {e}")





## for all the users send the summary report 
@shared_task
def enqueue_weekly_reports():
    """
    Find all active users and fire off one send_user_summary_report per user.
    """
    qs = User.objects.filter(is_active=True).values_list('id', flat=True)
    for uid in qs:
        send_user_summary_report.delay(uid, 'weekly')