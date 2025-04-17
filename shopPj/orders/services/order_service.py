from orders.models import OrderItem


def create_order_with_items(order, cart_items):
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
        )
