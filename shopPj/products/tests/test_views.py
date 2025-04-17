from django.test import TestCase, RequestFactory
from django.urls import reverse
from products.models import Product, Category
from products.views import ProductListView, ProductDetailView
from django.contrib.auth import get_user_model


class ProductListViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Test Category')
        self.product1 = Product.objects.create(name='Product 1', category=self.category, price=10.00)
        self.product2 = Product.objects.create(name='Test Product 2', category=self.category, price=20.00)

    def test_get_queryset_all_products(self):
        request = self.factory.get(reverse('product_list', kwargs={'category_id': self.category.id}))
        request.user = self.user
        view = ProductListView()
        view.request = request
        view.kwargs = {'category_id': self.category.id}
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 2)
        self.assertIn(self.product1, queryset)
        self.assertIn(self.product2, queryset)

    def test_get_queryset_by_category(self):
        request = self.factory.get(reverse('product_list', kwargs={'category_id': self.category.id}))
        request.user = self.user
        view = ProductListView()
        view.request = request
        view.kwargs = {'category_id': self.category.id}
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 2)
        self.assertEqual(view.category, self.category)

    def test_get_queryset_by_search_query(self):
        request = self.factory.get(
            reverse('product_list', kwargs={'category_id': self.category.id}) + '?search=Test'
        )
        request.user = self.user
        view = ProductListView()
        view.request = request
        view.kwargs = {'category_id': self.category.id}
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 1)
        self.assertIn(self.product2, queryset)

    def test_get_context_data(self):
        request = self.factory.get(
            reverse('product_list', kwargs={'category_id': self.category.id}) + '?search=Test'
        )
        request.user = self.user
        view = ProductListView()
        view.request = request
        view.kwargs = {'category_id': self.category.id}
        view.object_list = view.get_queryset()
        context = view.get_context_data()
        self.assertEqual(context['category'], self.category)
        self.assertEqual(context['search_query'], 'Test')
        self.assertEqual(context['products'].count(), 1)


class ProductDetailViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', category=self.category, price=10.00)

    def test_get_queryset(self):
        request = self.factory.get(reverse('product_detail', kwargs={'pk': self.product.pk}))
        request.user = self.user
        view = ProductDetailView()
        view.request = request
        view.kwargs = {'pk': self.product.pk}
        queryset = view.get_queryset()
        self.assertIn(self.product, queryset)