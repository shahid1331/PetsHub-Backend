from django.urls import path
from .views import ProductsByPriceAPIView

urlpatterns = [
    path('products/price/<int:price>/', ProductsByPriceAPIView.as_view()),
]
