from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .forms import OrderForm
from .models import OrderItem
from cart.models import Cart, CartItem
from orders.models import Order


@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def _get_cart_and_items(self, user):
        try:
            cart = Cart.objects.get(user=user, is_active=True)
            cart_items = CartItem.objects.filter(cart=cart)
            if not cart_items.exists():
                messages.warning(self.request, "Ваша корзина пуста. Добавьте товары, чтобы продолжить.")
                return None, None, None
            total_price = sum(item.product.price * item.quantity for item in cart_items)
            return cart, cart_items, total_price
        except Cart.DoesNotExist:
            messages.warning(self.request, "У вас нет активной корзины. Добавьте товары, чтобы продолжить.")
            return None, None, None

    def get(self, request, *args, **kwargs):
        cart, cart_items, total_price = self._get_cart_and_items(request.user)
        if not cart:
            return redirect('view_cart')

        form = OrderForm(user=request.user)
        return render(
            request,
            'orders/checkout.html',
            {'form': form, 'total_price': total_price},
        )

    def post(self, request, *args, **kwargs):
        cart, cart_items, total_price = self._get_cart_and_items(request.user)
        if not cart:
            return redirect('view_cart')

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
            messages.success(request, "Ваш заказ успешно оформлен!")
            return redirect('order_success')

        return render(
            request,
            'orders/checkout.html',
            {'form': form, 'total_price': total_price},
        )

@method_decorator(login_required, name='dispatch')
class OrderSuccessView(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user).order_by('-id').first()
        if not order:
            messages.warning(request, "У вас нет оформленных заказов.")
            return redirect('view_cart')

        order_items = order.order_items.all()
        total_price = sum(item.product.price * item.quantity for item in order_items)

        return render(
            request, 'orders/order_success.html', {
                'order': order,
                'order_items': order_items,
                'total_price': total_price
            }
        )
