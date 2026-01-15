from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from carts.models import CartItem
from .serializers import CartItemSerializer
from products.models import Product

class CreateListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(items,many=True)
        return Response(serializer.data)
    
class CartAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")

        if not product_id:
            return Response(
                {"error": "product_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id, active=True)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if product.stock <= 0:
            return Response(
                {"error": "Out of stock"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product
        )

        if not created:
            if cart_item.quantity + 1 > product.stock:
                return Response(
                    {"error": "Stock limit reached"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity += 1
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeleteCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            item = CartItem.objects.get(id=item_id, user=request.user)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        item.delete()
        return Response(
            {"message": "Item removed successfully"},
            status=status.HTTP_200_OK
        )

class CartUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        try:
            item = CartItem.objects.get(id=item_id, user=request.user)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        quantity = request.data.get("quantity")

        if quantity is None or int(quantity) < 1:
            return Response(
                {"error": "Quantity must be at least 1"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity > item.product.stock:
            return Response(
                {"error": "Stock limit exceeded"},
                status=status.HTTP_400_BAD_REQUEST
            )

        item.quantity = quantity
        item.save()

        return Response(
            {"message": "Quantity updated"},
            status=status.HTTP_200_OK
        )
