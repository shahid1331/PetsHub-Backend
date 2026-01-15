from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('dog', 'Dog'),
        ('cat', 'Cat'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.JSONField()
    price = models.IntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    rating = models.FloatField(default=0)
    stock = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
