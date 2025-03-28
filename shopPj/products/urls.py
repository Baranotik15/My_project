from django.urls import path
from .views import ProductListView

urlpatterns = [
    path(
        'category/<int:category_id>/',
        ProductListView.as_view(),
        name='product_list'
    ),
]