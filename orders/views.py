# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from django.db import transaction
# from rest_framework import serializers
# from .models import Order, OrderItem
# from products.models import Product
# from .serializers import OrderSerializer, OrderCreateSerializer


# class MyOrdersView(APIView):
#     permission_classes = [IsAuthenticated]

#     # 🔹 GET user's orders
#     def get(self, request):
#         orders = (
#             Order.objects
#             .filter(user=request.user)
#             .prefetch_related("items__product")
#             .order_by("-created_at")
#         )
#         serializer = OrderSerializer(orders, many=True)
#         return Response(serializer.data)

#     # 🔹 POST create order
#     @transaction.atomic
#     def post(self, request):
#         serializer = OrderCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         data = serializer.validated_data

#         # 1️⃣ Create order
#         order = Order.objects.create(
#             user=request.user,
#             name=data["name"],
#             address=data["address"],
#             phone=data["phone"],
#             payment_method=data["payment_method"],
#             total=data["total"],
#         )

#         # 2️⃣ Create items
#         for item in data["items"]:
#             try:
#                 product = Product.objects.get(id=item["product_id"])
#             except Product.DoesNotExist:
#                 raise serializers.ValidationError(
#                     f"Product {item['product_id']} does not exist"
#                 )

#             OrderItem.objects.create(
#                 order=order,
#                 product=product,
#                 quantity=item["quantity"],
#             )

#         return Response(
#             {
#                 "message": "Order created successfully",
#                 "order_id": order.id
#             },
#             status=status.HTTP_201_CREATED
#         )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers
from django.db import transaction

from .models import Order, OrderItem
from products.models import Product
from .serializers import OrderReadSerializer, OrderCreateSerializer


class MyOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = (
            Order.objects
            .filter(user=request.user)
            .prefetch_related("items__product")
            .order_by("-created_at")
        )
        serializer = OrderReadSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        order = Order.objects.create(
            user=request.user,
            name=data["name"],
            address=data["address"],
            phone=data["phone"],
            payment_method=data["payment_method"],
            total=0,  
        )

        total = 0

        for item in data["items"]:
            try:
                product = Product.objects.get(id=item["product_id"])
            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    f"Product {item['product_id']} does not exist"
                )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item["quantity"],
            )

            total += product.price * item["quantity"]
            
        order.total = total
        order.save()

        return Response(
            {
                "message": "Order created successfully",
                "order_id": order.id,
                "total": order.total,
            },
            status=status.HTTP_201_CREATED
        )
