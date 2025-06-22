from django.conf import settings
from core.mixins import TimeStampedModel
from django.db import models
from django.utils import timezone
from datetime import date
# Create your models here.

class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories') 
    
    class Meta:
        unique_together = ('name', 'user')
    def __str__(self):  
        return f"{self.name}  "
    
    

class Transaction(TimeStampedModel):
    class TransactionType(models.TextChoices):
        INCOME = 'I', 'Income'
        EXPENSE = 'E', 'Expense'
    type = models.CharField(max_length=1, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='transactions')
    date = models.DateField(default= timezone.localdate, null=False, blank=True)
    class Meta:
        ordering = ['-created_at']

        
    @property
    def is_income(self):
        return self.type == self.TransactionType.INCOME
    @property
    def is_expense(self):
        return self.type == self.TransactionType.EXPENSE
    
    @classmethod
    def incomes(cls):
        return cls.objects.filter(type=cls.TransactionType.INCOME)
    @classmethod
    def expenses(cls):
        return cls.objects.filter(type=cls.TransactionType.EXPENSE)
    
    def __str__(self):
        return f"{self.get_type_display()}: {self.amount} ({self.date})"
    

    