from django.urls import path
from .views import CheckoutView, OrderSuccessView

urlpatterns = [
    path(
        "checkout/",
        CheckoutView.as_view(),
        name="checkout"
    ),
    path(
        "order-success/<int:order_id>/",
        OrderSuccessView.as_view(),
        name="order_success"
    ),
]
