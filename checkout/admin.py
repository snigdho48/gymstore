from django.contrib import admin
from .models import Order, OrderLineItem
# Register your models here.


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'created',
                       'delivery_cost', 'grand_total',
                       'total', 'original_cart', 'stripe_pid')

    fields = ('order_number', 'user_profile', 'created', 'billingName',
              'emailAddress', 'billingAdress1', 'billingCity',
              'billingPostcode', 'billingCountry', 'shippingName',
              'shippingAddress1', 'shippingCity', 'shippingPostcode',
              'shippingCountry', 'total', 'grand_total', 'delivery_cost',
              'original_cart', 'stripe_pid')

    listdisplay = ('order_number', 'created', 'billingName',
                   'grand_total', 'delivery_cost', 'total',)

    ordering = ('-created',)


admin.site.register(Order, OrderAdmin)