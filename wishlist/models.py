from django.db import models
from products.models import Product
from accounts.models import RegisterUser

class Wishlist(models.Model):
    user = models.ForeignKey(
        RegisterUser,
        on_delete=models.CASCADE,
        related_name='wishlist'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"