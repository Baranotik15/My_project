from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from products.models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.kwargs.get('category_id')
        search_query = self.request.GET.get('search', '')

        if category_id:
            category = get_object_or_404(Category, id=category_id)
            queryset = queryset.filter(category=category)

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset # Не пойму почему не учитывает регистры вроде айконтейнс должен, но не рабоатет

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')

        if category_id:
            category = get_object_or_404(Category, id=category_id)
            context['category'] = category

        context['search_query'] = self.request.GET.get('search', '')

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'products_detail'
