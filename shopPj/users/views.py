from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import Product


class FavoriteListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "users/favorites.html"
    context_object_name = "favorites"

    def get_queryset(self):
        return Product.objects.filter(favorite_products=self.request.user)


class AddToFavoritesView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        request.user.favorite_products.add(product)
        return redirect('product_detail', pk=product.id)


class RemoveFromFavoritesView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)

        if product in request.user.favorite_products.all():
            request.user.favorite_products.remove(product)
            return redirect('favorites')
        else:
            return redirect('product_detail', pk=product.id)
