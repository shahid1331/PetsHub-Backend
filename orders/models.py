from django.db import models
from accounts.models import RegisterUser
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(RegisterUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name="items",on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
