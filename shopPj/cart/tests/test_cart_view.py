from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from cart.models import Cart, CartItem, Product
from cart.views import CartItemDeleteView


class CartViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

        self.product1 = Product.objects.create(name="Product 1", price=10)
        self.product2 = Product.objects.create(name="Product 2", price=20)

        self.cart = Cart.objects.create(user=self.user, is_active=True)

        self.cart_item1 = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        self.cart_item2 = CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)

        self.url = reverse('view_cart')

    def test_get_queryset(self):
        response = self.client.get(self.url)
        cart_items = response.context['cart_items']

        self.assertEqual(cart_items.count(), 2)
        self.assertEqual(cart_items[0], self.cart_item1)
        self.assertEqual(cart_items[1], self.cart_item2)

    def test_get_total_price(self):
        expected_total_price = (self.product1.price * self.cart_item1.quantity) + (
                    self.product2.price * self.cart_item2.quantity)

        response = self.client.get(self.url)

        self.assertEqual(response.context['total_price'], expected_total_price)

    def test_get_context_data(self):
        response = self.client.get(self.url)

        self.assertIn('total_price', response.context)
        self.assertEqual(response.context['total_price'], 40)


class AddToCartViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.product = Product.objects.create(name="Test Product", price=50)

        self.client.login(username="testuser", password="testpassword")
        self.url = reverse('add_to_cart', args=[self.product.id])

    def test_add_new_product_creates_cart_and_cart_item(self):
        response = self.client.post(self.url)

        cart = Cart.objects.get(user=self.user, is_active=True)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)

        self.assertRedirects(response, reverse('view_cart'))
        self.assertEqual(cart_item.quantity, 1)

    def test_add_existing_product_increases_quantity(self):
        self.client.post(self.url)
        self.client.post(self.url)

        cart = Cart.objects.get(user=self.user, is_active=True)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)

        self.assertEqual(cart_item.quantity, 2)


class CartItemDeleteViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = get_user_model().objects.create_user(username="user1", password="pass")
        self.user2 = get_user_model().objects.create_user(username="user2", password="pass")

        self.product = Product.objects.create(name="Test Product", price=10)

        self.cart1 = Cart.objects.create(user=self.user1, is_active=True)
        self.cart2 = Cart.objects.create(user=self.user2, is_active=True)

        self.cart_item1 = CartItem.objects.create(cart=self.cart1, product=self.product, quantity=1)
        self.cart_item2 = CartItem.objects.create(cart=self.cart2, product=self.product, quantity=1)

    def test_get_queryset_returns_only_user_cart_items(self):
        request = self.factory.get("/")
        request.user = self.user1

        view = CartItemDeleteView()
        view.request = request

        queryset = view.get_queryset()

        self.assertIn(self.cart_item1, queryset)
        self.assertNotIn(self.cart_item2, queryset)


