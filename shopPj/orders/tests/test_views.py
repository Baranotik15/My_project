from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from orders.models import Order
from cart.models import Cart, CartItem
from products.models import Product
from unittest.mock import patch


class CheckoutViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.product = Product.objects.create(name="Test Product", price=100)
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_checkout_view_get(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/checkout.html')


class OrderSuccessViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.order = Order.objects.create(user=self.user, payment_method='cash', status=Order.OrderStatus.PENDING)

    @patch('orders.services.stripe_service.verify_stripe_payment')
    def test_order_success_view_stripe_payment(self, mock_verify_stripe_payment):
        mock_verify_stripe_payment.return_value = (None, None)
        response = self.client.get(reverse('order_success', kwargs={'order_id': self.order.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_success.html')

    def test_order_success_view(self):
        response = self.client.get(reverse('order_success', kwargs={'order_id': self.order.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_success.html')