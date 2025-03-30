from django.urls import path
from .views import (
    CartView,
    CartItemDeleteView,
    AddToCartView,
    UpdateCartItemQuantityView,
)

urlpatterns = [
    path(
        "",
        CartView.as_view(),
        name="view_cart"
    ),
    path(
        "delete/<int:pk>/",
        CartItemDeleteView.as_view(),
        name="delete_cart_item"
    ),
    path(
        "add_to_cart/<int:product_id>/",
        AddToCartView.as_view(),
        name="add_to_cart"
    ),
    path(
        "update_cart_item/<int:cart_item_id>/<str:action>/",
        UpdateCartItemQuantityView.as_view(),
        name="update_cart_item_quantity",
    ),
]
