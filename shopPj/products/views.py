from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from products.models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 8

    def get_queryset(self):
        queryset = Product.objects.select_related("category")
        self.category = None

        category_id = self.kwargs.get("category_id")
        search_query = self.request.GET.get("search", "")

        if category_id:
            self.category = get_object_or_404(Category, id=category_id)
            queryset = queryset.filter(category=self.category)

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["search_query"] = self.request.GET.get("search", "")
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "products_detail"

    def get_queryset(self):
        return Product.objects.select_related("category")
