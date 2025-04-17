from django.test import TestCase
from orders.models import Order, OrderItem
from products.models import Product
from django.contrib.auth import get_user_model


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", password="1234"
        )
        self.product = Product.objects.create(
            name="Test Product",
            price=100.0,
            stock=10
        )
        self.order = Order.objects.create(user=self.user)

    def test_get_price(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3
        )
        self.assertEqual(order_item.get_price(), 300.0)


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", password="1234"
        )
        self.product = Product.objects.create(
            name="Test Product",
            price=100.0,
            stock=10
        )
        self.order = Order.objects.create(
            user=self.user,
            status=Order.OrderStatus.PENDING,
            delivery_method="Delivery",
            payment_method="stripe",
            full_name="Test User",
            phone_number="123456789"
        )
        self.order_item1 = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2
        )
        self.order_item2 = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3
        )

    def test_get_total_price(self):
        expected_total_price = (self.product.price * self.order_item1.quantity) + (
            self.product.price * self.order_item2.quantity
        )
        self.assertEqual(self.order.get_total_price(), expected_total_price)
