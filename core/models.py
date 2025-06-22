from django.db import models
from django.conf import settings 
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    class Role(models.TextChoices):
        ROLE_ADMIN = 'A', 'Admin'
        ROLE_MANAGER = 'M', 'Manager'
        ROLE_USER = 'U', 'User'

    role = models.CharField(max_length=1, choices=Role, default=Role.ROLE_USER)
    email = models.EmailField(unique=True, blank=False, null=False)
    
    # Flags
    is_premium = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    def __str__(self):
        return self.email  
    

    
    
    
    

    
# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     image = models.ImageField(upload_to='products/')
    
#     def __str__(self):
#         return f"{self.name} - ${self.price}"
    

# class Order(models.Model):
#     STATUS_PENDING = 'P'
#     STATUS_COMPLETED = 'C'
#     STATUS_CANCELLED = 'X'
#     STATUS_CHOICES = [
#         (STATUS_PENDING, 'Pending'),
#         (STATUS_COMPLETED, 'Completed'),
#         (STATUS_CANCELLED, 'Cancelled'),
#     ]
    
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_PENDING) 
#     products = models.ManyToManyField(Product, through='OrderItem')   
    
#     def __str__(self):
#         return f"Order {self.id} by {self.user.username} - Status: {self.get_status}"
    
    
    
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
    
    
#     def __str__(self):
#         return f"{self.quantity} x {self.product.name} in Order {self.order.id}"