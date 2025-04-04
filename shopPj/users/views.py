from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from orders.models import Order
from products.models import Product


class FavoriteListView(LoginRequiredMixin, ListView):
    template_name = "users/favorites.html"
    context_object_name = "favorites"

    def get_queryset(self):
        return Product.objects.filter(favorite_products=self.request.user)


class AddToFavoritesView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        request.user.favorite_products.add(product)
        return redirect("product_detail", pk=product.id)


class RemoveFromFavoritesView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)

        if product in request.user.favorite_products.all():
            request.user.favorite_products.remove(product)
            return redirect("favorites")
        else:
            return redirect("product_detail", pk=product.id)


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        orders = Order.objects.filter(user=user).order_by("-created_at")

        orders_with_details = []
        for order in orders:
            order_items = order.order_items.all()
            total_price = (
                order.total_price
                if hasattr(order, "total_price")
                else sum(
                    item.quantity * item.product.price
                    for item in order_items
                )
            )
            orders_with_details.append(
                {
                    "order": order,
                    "order_items": order_items,
                    "total_price": total_price
                }
            )

        return render(
            request,
            "users/profile.html",
            {
                "user": user,
                "orders": orders_with_details,
            },
        )
