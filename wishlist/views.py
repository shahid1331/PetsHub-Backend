# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist, Product
from .serializers import WishlistSerializer
from rest_framework import status

class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist, many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get("product_id")
        product = Product.objects.get(id=product_id)

        Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        return Response({"message": "Added to wishlist"})

    # def delete(self, request, product_id):
    #     Wishlist.objects.filter(
    #         user=request.user,
    #         product_id=product_id
    #     ).delete()
    #     return Response({"message": "Removed from wishlist"})
    
    def delete(self, request, product_id):
        try:
            item = Wishlist.objects.get(id=product_id, user=request.user)
        except Wishlist.DoesNotExist:
            return Response(
                {"error": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        item.delete()
        return Response(
            {"message": "Item removed successfully"},
            status=status.HTTP_200_OK
        )
