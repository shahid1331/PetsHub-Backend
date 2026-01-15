from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemReadSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["name", "quantity"]

class OrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)
    date = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "total",
            "date",
            "items",
        ]


class OrderItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    address = serializers.CharField()
    phone = serializers.CharField()
    payment_method = serializers.CharField()
    items = OrderItemCreateSerializer(many=True)
