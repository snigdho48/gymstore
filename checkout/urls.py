from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),  # noqa:501
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),  # noqa:501
    path('wh/', webhook, name='webhook'),
]
