from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('', views.all_products, name='products'),
    path('<product_id>', views.product_detail, name='product_detail'),
    path('category/<category_id>', views.filter_products_by_category, name='product_category'),  # noqa:501
]
