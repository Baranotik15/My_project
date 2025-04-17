from django.contrib import messages
from cart.models import Cart, CartItem


def get_cart_and_items(request, user):
    try:
        cart = Cart.objects.get(user=user, is_active=True)
        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            messages.warning(request, "Ваша корзина пуста. Добавьте товары, чтобы продолжить.")
            return None, None, None
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return cart, cart_items, total_price
    except Cart.DoesNotExist:
        messages.warning(request, "У вас нет активной корзины. Добавьте товары, чтобы продолжить.")
        return None, None, None
