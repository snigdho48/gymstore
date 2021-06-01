from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('billingName', 'emailAddress', 'phone',
                  'billingAdress1', 'billingCity', 'billingPostcode',
                  'billingCountry', 'shippingName', 'shippingAddress1',
                  'shippingCity', 'shippingPostcode', 'shippingCountry', 'total',  # noqa:501
                  )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'billingName': 'Billing Name',
            'emailAddress': 'Email',
            'phone': 'Phone Number',
            'billingAdress1': 'Billing Adress1',
            'billingCity': 'Billing City',
            'billingPostcode': 'Billing Postcode',
            'billingCountry': 'Billing Country',
            'shippingName': 'Shipping Name',
            'shippingAddress1': 'Shipping Address1',
            'shippingCity': 'Shipping City',
            'shippingPostcode': 'Shipping Postcode',
            'shippingCountry': 'Shipping Country',
            'total': 'Order Total',
        }

        self.fields['billingName'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False