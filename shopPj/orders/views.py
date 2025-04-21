from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from orders.forms import OrderForm
from orders.models import Order
from orders.services.stripe_service import create_stripe_checkout_session, verify_stripe_payment
from orders.services.cart_service import get_cart_and_items
from orders.models import OrderItem


def create_order_with_items(order, cart_items):
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
        )


@method_decorator(login_required, name="dispatch")
class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        cart, cart_items, total_price = get_cart_and_items(request, request.user)
        if not cart:
            return redirect("view_cart")

        form = OrderForm(user=request.user)
        return render(request, "orders/checkout.html", {
            "form": form,
            "total_price": total_price,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        })

    def post(self, request, *args, **kwargs):
        cart, cart_items, total_price = get_cart_and_items(request, request.user)
        if not cart:
            return redirect("view_cart")

        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save()
            create_order_with_items(order, cart_items)

            cart.is_active = False
            cart.save()

            if form.cleaned_data["payment_method"] == "cart":
                try:
                    session = create_stripe_checkout_session(request, order, total_price)
                    order.stripe_session_id = session.id
                    order.save()
                    messages.success(request, "Переходите к оплате!")
                    return redirect(session.url, code=303)
                except Exception as e:
                    messages.error(request, f"Ошибка оплаты: {str(e)}")
                    return redirect("checkout")

            messages.success(request, "Заказ оформлен! Оплатите наличными при получении.")
            return redirect(reverse("order_success", kwargs={"order_id": order.id}))

        return render(request, "orders/checkout.html", {
            "form": form,
            "total_price": total_price,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        })


@method_decorator(login_required, name="dispatch")
class OrderSuccessView(View):
    def get(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id, user=request.user)

        if order.payment_method == "cart" and order.stripe_session_id:
            payment_intent, error = verify_stripe_payment(order)
            if error:
                messages.error(request, error)
                return redirect("view_cart")
            if payment_intent and not order.stripe_payment_intent:
                order.stripe_payment_intent = payment_intent.id
                order.save()

        if order.status == Order.OrderStatus.PENDING:
            order.status = Order.OrderStatus.COMPLETED
            order.save()

        return render(request, "orders/order_success.html", {
            "order": order,
            "order_items": order.order_items.all(),
            "total_price": order.get_total_price(),
        })


@method_decorator(login_required, name="dispatch")
class PaymentCancelView(View):
    def get(self, request, *args, **kwargs):
        messages.info(request, "Оплата была отменена.")
        return redirect("view_cart")
