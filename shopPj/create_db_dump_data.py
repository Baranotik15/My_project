import os
import django
from django.core.management import call_command
from django.db import connection

os.environ['DJANGO_SETTINGS_MODULE'] = 'shopPj.settings.dev'
django.setup()


def clean_database():
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM orders_orderitem 
            WHERE order_id NOT IN (SELECT id FROM orders_order)
        """)

        cursor.execute("""
            DELETE FROM cart_cartitem 
            WHERE cart_id NOT IN (SELECT id FROM cart_cart)
        """)

        cursor.execute("""
            DELETE FROM cart_cartitem 
            WHERE product_id NOT IN (SELECT id FROM products_product)
        """)

        cursor.execute("""
            DELETE FROM orders_order 
            WHERE user_id NOT IN (SELECT id FROM users_user)
        """)

        cursor.execute("""
            DELETE FROM orders_orderitem 
            WHERE product_id NOT IN (SELECT id FROM products_product)
        """)


def export_data():
    print("Экспорт данных в JSON...")
    with open('data.json', 'w', encoding='utf-8') as f:
        call_command(
            'dumpdata',
            'users',
            'products',
            'orders',
            'cart',
            'core',
            '--natural-foreign',
            '--natural-primary',
            stdout=f,
            indent=2,
            format='json',
        )
    print("Данные успешно экспортированы в data.json")


if __name__ == "__main__":
    clean_database()
    export_data()