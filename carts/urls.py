from django.urls import path 
from .views import CreateListView,CartAddView,DeleteCartView,CartUpdateView

urlpatterns = [
    path('cart/',CreateListView.as_view()),
    path('cart/add/',CartAddView.as_view()),
    path('cart/update/<int:item_id>/',CartUpdateView.as_view()),
    path('cart/delete/<int:item_id>/',DeleteCartView.as_view()),
]
