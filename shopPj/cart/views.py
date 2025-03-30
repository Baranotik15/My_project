from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView
from cart.models import Cart, CartItem
from products.models import Product


class CartView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = "cart/view_cart.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(
            user=self.request.user, is_active=True
        )
        return CartItem.objects.filter(cart=cart)

    def get_total_price(self):
        total_price = sum(
            item.product.price * item.quantity
            for item in self.get_queryset()
        )
        return total_price

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_price"] = self.get_total_price()
        return context


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(
            Product,
            id=product_id
        )
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            is_active=True
        )
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect("view_cart")


class CartItemDeleteView(LoginRequiredMixin, DeleteView):
    model = CartItem
    template_name = "cart/cart_item_confirm_delete.html"
    context_object_name = "cart_item"
    success_url = reverse_lazy("view_cart")

    def get_queryset(self):
        return CartItem.objects.filter(
            cart__user=self.request.user,
            cart__is_active=True
        )


class UpdateCartItemQuantityView(LoginRequiredMixin, View):
    def post(self, request, cart_item_id, action):
        cart_item = get_object_or_404(
            CartItem,
            id=cart_item_id,
            cart__user=request.user,
            cart__is_active=True
        )

        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()

        return redirect("view_cart")
