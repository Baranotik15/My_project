from django import forms
from django.db import models
from .models import Order

class OrderForm(forms.ModelForm):
    class DeliveryChoices(models.TextChoices):
        PICKUP = 'Pickup', 'Pickup'
        DELIVERY = 'Delivery', 'Delivery'

    class PaymentChoices(models.TextChoices):
        CREDIT_CARD = 'credit_card', 'Credit Card'
        PAYPAL = 'paypal', 'PayPal'
        IN_CASH = 'in_cash', 'In Cash'

    pickup_address = forms.ChoiceField(
        choices=[
            ('store1', 'Store 1'),
            ('store2', 'Store 2'),
            ('store3', 'Store 3')
        ],
        required=False,
        widget=forms.RadioSelect,
    )

    delivery_address = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
            'placeholder': 'Enter delivery address'
            }
        ),
    )

    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter phone number'
            }
        ),
    )

    full_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter full name'
            }
        ),
    )

    delivery_method = forms.ChoiceField(
        choices=DeliveryChoices.choices,
        required=True,
        initial='Pickup',
    )
    payment_method = forms.ChoiceField(
        choices=PaymentChoices.choices,
        required=True,
    )

    class Meta:
        model = Order
        fields = [
            'delivery_method',
            'payment_method',
            'pickup_address',
            'delivery_address',
            'phone_number',
            'full_name',
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        delivery_method = cleaned_data.get('delivery_method')
        pickup_address = cleaned_data.get('pickup_address')
        delivery_address = cleaned_data.get('delivery_address')
        phone_number = cleaned_data.get('phone_number')
        full_name = cleaned_data.get('full_name')

        if not phone_number:
            self.add_error('phone_number', 'Phone number is required.')
        if not full_name:
            self.add_error('full_name', 'Full name is required.')

        if delivery_method == 'Delivery' and not delivery_address:
            self.add_error('delivery_address', 'Delivery address is required.')
        if delivery_method == 'Pickup' and not pickup_address:
            self.add_error('pickup_address', 'Please select a pickup store.')

        return cleaned_data

    def save(self, commit=True):
        order = super().save(commit=False)
        if self.user:
            order.user = self.user
        if commit:
            order.save()
        return order
