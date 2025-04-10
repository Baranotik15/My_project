from django.core.management.base import BaseCommand
from orders.models import Order
import stripe
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Проверяет статус незавершенных заказов через Stripe API'

    def handle(self, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.stdout.write(f"Using Stripe API key: {settings.STRIPE_SECRET_KEY[:10]}...")
        logger.info(f"Using Stripe API key: {settings.STRIPE_SECRET_KEY[:10]}...")

        self.stdout.write("Начало проверки незавершенных заказов")
        logger.info("Начало проверки незавершенных заказов")

        pending_orders = Order.objects.filter(
            status=Order.OrderStatus.PENDING,
            stripe_session_id__isnull=False
        )
        self.stdout.write(f"Найдено заказов: {pending_orders.count()}")
        logger.info(f"Найдено заказов: {pending_orders.count()}")

        for order in pending_orders:
            self.stdout.write(f"Проверка заказа {order.id}, stripe_session_id: {order.stripe_session_id}")
            logger.info(f"Проверка заказа {order.id}, stripe_session_id: {order.stripe_session_id}")
            try:
                session = stripe.checkout.Session.retrieve(order.stripe_session_id)
                if not session.payment_intent:
                    self.stdout.write(f"Заказ {order.id}: PaymentIntent ещё не создан")
                    logger.info(f"Заказ {order.id}: PaymentIntent ещё не создан")
                    continue

                payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)
                self.stdout.write(f"Статус PaymentIntent: {payment_intent.status}")
                logger.info(f"Статус PaymentIntent: {payment_intent.status}")

                order.stripe_payment_intent = session.payment_intent
                order.save()

                if payment_intent.status == "succeeded":
                    order.status = Order.OrderStatus.COMPLETED
                    self.stdout.write(
                        self.style.SUCCESS(f"Заказ {order.id} подтвержден как оплаченный")
                    )
                    logger.info(f"Заказ {order.id} подтвержден как оплаченный")
                else:
                    order.status = Order.OrderStatus.PENDING
                    self.stdout.write(
                        f"Заказ {order.id} не оплачен, статус: {payment_intent.status}"
                    )
                    logger.info(f"Заказ {order.id} не оплачен, статус: {payment_intent.status}")
                order.save()
                self.stdout.write(f"Сохранён заказ {order.id} с новым статусом: {order.status}")
                logger.info(f"Сохранён заказ {order.id} с новым статусом: {order.status}")
            except stripe.error.StripeError as e:
                self.stdout.write(
                    self.style.ERROR(f"Ошибка проверки заказа {order.id}: {str(e)}")
                )
                logger.error(f"Ошибка проверки заказа {order.id}: {str(e)}")
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Неизвестная ошибка для заказа {order.id}: {str(e)}")
                )
                logger.error(f"Неизвестная ошибка для заказа {order.id}: {str(e)}")

        self.stdout.write(self.style.SUCCESS("Проверка заказов завершена"))
        logger.info("Проверка заказов завершена")
