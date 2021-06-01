import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile


# Model: Order
class Order(models.Model):
    order_number = models.CharField(max_length=35, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')  # noqa:501
    billingName = models.CharField(max_length=250, blank=True)
    emailAddress = models.EmailField(max_length=250, blank=True, verbose_name='Email Adress')  # noqa:501
    phone = models.CharField(max_length=15, null=False, default=0)
    billingCountry =  CountryField(blank_label='Country *', null=False, blank=False)  # noqa:501
    billingPostcode = models.CharField(max_length=250, blank=True)
    billingCity = models.CharField(max_length=250, blank=True)
    billingAdress1 = models.CharField(max_length=250, blank=True)
    shippingName = models.CharField(max_length=250, blank=True)
    shippingAddress1 = models.CharField(max_length=250, blank=True)
    shippingCity = models.CharField(max_length=250, blank=True)
    shippingPostcode = models.CharField(max_length=250, blank=True)
    shippingCountry =  CountryField(blank_label='Country *', null=False, blank=False) # noqa:501
    created = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)  # noqa:501
    total = models.DecimalField(max_digits=10, null=True, decimal_places=2, verbose_name='USD Order Total')  # noqa:501
    grand_total = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)  # noqa:501
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')  # noqa:501

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def update_total(self):
        self.total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0  # noqa:501
        if self.total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.total * settings.STANDARD_DELIVERY_PERCENTAGE / 100  # noqa:501
        else:
            self.delivery_cost = 0
            self.total = self.total + self.delivery_cost
            self.save()

    def save(self, *args, **kwargs):

        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')  # noqa:501
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)   # noqa:501
    product_size = models.CharField(max_length=2, null=True, blank=True)  # XS, S, M, L, XL   # noqa:501
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)   # noqa:501

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
