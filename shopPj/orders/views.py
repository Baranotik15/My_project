import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .forms import OrderForm
from .models import OrderItem
from cart.models import Cart, CartItem
from orders.models import Order


stripe.api_key = settings.STRIPE_SECRET_KEY


@method_decorator(login_required, name="dispatch")
class CheckoutView(View):
    def _get_cart_and_items(self, user):
        try:
            cart = Cart.objects.get(user=user, is_active=True)
            cart_items = CartItem.objects.filter(cart=cart)
            if not cart_items.exists():
                messages.warning(
                    self.request,
                    "Ваша корзина пуста."
                    " Добавьте товары, чтобы продолжить.",
                )
                return None, None, None
            total_price = sum(item.product.price * item.quantity for item in cart_items)
            return cart, cart_items, total_price
        except Cart.DoesNotExist:
            messages.warning(
                self.request,
                "У вас нет активной корзины. Добавьте товары, чтобы продолжить.",
            )
            return None, None, None

    def get(self, request, *args, **kwargs):
        cart, cart_items, total_price = self._get_cart_and_items(request.user)
        if not cart:
            return redirect("view_cart")

        form = OrderForm(user=request.user)
        context = {
            "form": form,
            "total_price": total_price,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        }
        return render(request, "orders/checkout.html", context)

    def post(self, request, *args, **kwargs):
        cart, cart_items, total_price = self._get_cart_and_items(request.user)
        if not cart:
            return redirect("view_cart")

        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save()
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                )

            cart.is_active = False
            cart.save()

            payment_method = form.cleaned_data["payment_method"]
            if payment_method == "stripe":
                try:
                    session = stripe.checkout.Session.create(
                        payment_method_types=["card"],
                        line_items=[
                            {
                                "price_data": {
                                    "currency": "usd",
                                    "product_data": {
                                        "name": f"Order {order.id}",
                                    },
                                    "unit_amount": int(total_price * 100),
                                },
                                "quantity": 1,
                            }
                        ],
                        mode="payment",
                        success_url=request.build_absolute_uri(
                            reverse("order_success")
                        ),
                        cancel_url=request.build_absolute_uri(
                            "/payment-cancel/"
                        ),
                        metadata={"order_id": order.id},
                    )

                    order.stripe_payment_intent = session.payment_intent
                    order.save()

                    messages.success(request, "Переходите к оплате!")
                    return redirect(session.url, code=303)
                except stripe.error.StripeError as e:
                    messages.error(request, f"Ошибка оплаты: {str(e)}")
                    return redirect("checkout")
            else:
                messages.success(
                    request,
                    "Заказ оформлен! Оплатите наличными при получении."
                )
                return redirect("order_success")

        context = {
            "form": form,
            "total_price": total_price,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        }
        return render(
            request,
            "orders/checkout.html",
            context
        )


@method_decorator(login_required, name="dispatch")
class OrderSuccessView(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(
            user=request.user
        ).order_by("-id").first()

        if not order:
            messages.warning(
                request,
                "У вас нет оформленных заказов."
            )
            return redirect("view_cart")

        if order.status == Order.OrderStatus.PENDING:
            order.status = Order.OrderStatus.COMPLETED
            order.save()

        order_items = order.order_items.all()

        context = {
            "order": order,
            "order_items": order_items,
            "total_price":  order.total_price,
        }

        return render(
            request,
            "orders/order_success.html",
            context
        )


@method_decorator(login_required, name="dispatch")
class PaymentCancelView(View):
    def get(self, request, *args, **kwargs):
        messages.info(request, "Оплата была отменена.")
        return redirect("view_cart")
