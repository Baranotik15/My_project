from django.test import TestCase
from orders.forms import OrderForm
from django.contrib.auth import get_user_model


class OrderFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )

    def test_valid_pickup_order(self):
        form_data = {
            "delivery_method": "Pickup",
            "payment_method": "stripe",
            "pickup_address": "store1",
            "phone_number": "1234567890",
            "full_name": "John Doe",
        }
        form = OrderForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
        order = form.save()
        self.assertEqual(order.user, self.user)

    def test_valid_delivery_order(self):
        form_data = {
            "delivery_method": "Delivery",
            "payment_method": "in_cash",
            "delivery_address": "123 Main St",
            "phone_number": "0987654321",
            "full_name": "Jane Smith",
        }
        form = OrderForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
        order = form.save()
        self.assertEqual(order.user, self.user)

    def test_missing_delivery_address_for_delivery_method(self):
        form_data = {
            "delivery_method": "Delivery",
            "payment_method": "stripe",
            "delivery_address": "",
            "phone_number": "1234567890",
            "full_name": "John Doe",
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("delivery_address", form.errors)

    def test_missing_pickup_address_for_pickup_method(self):
        form_data = {
            "delivery_method": "Pickup",
            "payment_method": "stripe",
            "pickup_address": "",
            "phone_number": "1234567890",
            "full_name": "John Doe",
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("pickup_address", form.errors)

    def test_stripe_token_optional(self):
        form_data = {
            "delivery_method": "Pickup",
            "payment_method": "stripe",
            "pickup_address": "store2",
            "phone_number": "5555555555",
            "full_name": "Alice",
            "stripe_token": "",
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())
