from django.urls import path
from products.views import ProductListView, ProductDetailView

urlpatterns = [
    path(
        "categories/<int:category_id>/",
        ProductListView.as_view(),
        name="product_list"
    ),
    path(
        "products/<int:pk>/",
        ProductDetailView.as_view(),
        name="product_detail"
    ),
]
