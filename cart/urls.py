from django.urls import path
from . import views

urlpatterns = [
    path('', views.shopping_cart, name='cart'),
    path('cart/add/<int:product_id>', views.add_cart, name='add_cart'),
    path('cart', views.cart_detail, name='cart_detail'),
    path('cart/remove/<int:product_id>', views.cart_remove, name='cart_remove'),  # noqa:501
    path('cart/remove_product/<int:product_id>', views.cart_remove_product, name='cart_remove_product'),  # noqa:501
]
