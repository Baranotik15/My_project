import stripe
from django.conf import settings
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_checkout_session(request, order, total_price):
    return stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "uah",
                    "product_data": {"name": f"Order {order.id}"},
                    "unit_amount": int(total_price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("order_success", kwargs={"order_id": order.id})
        ),
        cancel_url=request.build_absolute_uri("/payment-cancel/"),
        metadata={"order_id": order.id},
    )


def verify_stripe_payment(order):
    session = stripe.checkout.Session.retrieve(order.stripe_session_id)
    if not session.payment_intent:
        return None, "Оплата ещё не начата."

    payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)
    if payment_intent.status != "succeeded" and order.status == order.OrderStatus.PENDING:
        return None, "Оплата не была завершена."

    return payment_intent, None
