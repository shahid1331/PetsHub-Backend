from rest_framework import serializers
from .models import CartItem

class CartItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="product.name", read_only=True)
    image = serializers.JSONField(source="product.image", read_only=True)
    price = serializers.IntegerField(source="product.price", read_only=True)
    category = serializers.CharField(source="product.category", read_only=True)
    stock = serializers.IntegerField(source="product.stock", read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "name",
            "image",
            "price",
            "category",
            "stock",
            "quantity",
        ]