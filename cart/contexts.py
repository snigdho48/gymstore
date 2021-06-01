from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from cart.models import Cart, CartItem


def cart_contents(request):
    try:
        cart_items = []
        total = 0
        product_count = 0
        cart_id = request.session.session_key
        cart = Cart.objects.get(cart_id=cart_id)
        items = CartItem.objects.filter(cart=cart)
        for item in items:
            total += item.quantity * item.product.price
            product_count += item.quantity
            cart_items.append({
                'item_id': item.pk,
                'quantity': item.quantity,
                'product': item.product
            })
    except:
        pass

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
