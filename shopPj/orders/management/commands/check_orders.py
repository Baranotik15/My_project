from django.core.management.base import BaseCommand
from orders.models import Order
import stripe
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Checks the status of pending orders via the Stripe API'

    def handle(self, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.stdout.write(f"Using Stripe API key: {settings.STRIPE_SECRET_KEY[:10]}...")
        logger.info(f"Using Stripe API key: {settings.STRIPE_SECRET_KEY[:10]}...")

        self.stdout.write("Starting check of pending orders")
        logger.info("Starting check of pending orders")

        pending_orders = Order.objects.filter(
            status=Order.OrderStatus.PENDING,
            stripe_session_id__isnull=False
        )
        self.stdout.write(f"Found orders: {pending_orders.count()}")
        logger.info(f"Found orders: {pending_orders.count()}")

        for order in pending_orders:
            self.stdout.write(f"Checking order {order.id}, stripe_session_id: {order.stripe_session_id}")
            logger.info(f"Checking order {order.id}, stripe_session_id: {order.stripe_session_id}")
            try:
                session = stripe.checkout.Session.retrieve(order.stripe_session_id)
                if not session.payment_intent:
                    self.stdout.write(f"Order {order.id}: PaymentIntent has not been created yet")
                    logger.info(f"Order {order.id}: PaymentIntent has not been created yet")
                    continue

                payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)
                self.stdout.write(f"PaymentIntent status: {payment_intent.status}")
                logger.info(f"PaymentIntent status: {payment_intent.status}")

                order.stripe_payment_intent = session.payment_intent
                order.save()

                if payment_intent.status == "succeeded":
                    order.status = Order.OrderStatus.COMPLETED
                    self.stdout.write(
                        self.style.SUCCESS(f"Order {order.id} confirmed as paid")
                    )
                    logger.info(f"Order {order.id} confirmed as paid")
                else:
                    order.status = Order.OrderStatus.PENDING
                    self.stdout.write(
                        f"Order {order.id} not paid, status: {payment_intent.status}"
                    )
                    logger.info(f"Order {order.id} not paid, status: {payment_intent.status}")
                order.save()
                self.stdout.write(f"Order {order.id} saved with new status: {order.status}")
                logger.info(f"Order {order.id} saved with new status: {order.status}")
            except stripe.error.StripeError as e:
                self.stdout.write(
                    self.style.ERROR(f"Error checking order {order.id}: {str(e)}")
                )
                logger.error(f"Error checking order {order.id}: {str(e)}")
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Unknown error for order {order.id}: {str(e)}")
                )
                logger.error(f"Unknown error for order {order.id}: {str(e)}")

        self.stdout.write(self.style.SUCCESS("Order check completed"))
        logger.info("Order check completed")
