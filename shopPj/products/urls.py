from django.urls import path
from products.views import ProductListView, ProductDetailView

urlpatterns = [
    path(
        "category/<int:category_id>/",
        ProductListView.as_view(),
        name="product_list"
    ),
    path(
        "product/<int:pk>/",
        ProductDetailView.as_view(),
        name="product_detail"
    ),
]
