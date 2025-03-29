from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import OrderForm
from .models import OrderItem
from cart.models import Cart, CartItem


@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user, is_active=True)
            cart_items = CartItem.objects.filter(cart=cart)
            if not cart_items.exists():
                return redirect('view_cart')
        except Cart.DoesNotExist:
            return redirect('view_cart')

        total_price = sum(item.product.price * item.quantity for item in cart_items)
        form = OrderForm(user=request.user)
        return render(
            request,
            'orders/checkout.html',
            {'form': form, 'total_price': total_price},
        )

    def post(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user, is_active=True)
            cart_items = CartItem.objects.filter(cart=cart)
            if not cart_items.exists():
                return redirect('view_cart')
        except Cart.DoesNotExist:
            return redirect('view_cart')

        total_price = sum(item.product.price * item.quantity for item in cart_items)
        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save()
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )
            cart.is_active = False
            cart.save()
            return redirect('order_success')

        return render(
            request,
            'orders/checkout.html',
            {'form': form, 'total_price': total_price},
        )
