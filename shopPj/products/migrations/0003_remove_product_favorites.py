# Generated by Django 5.1.7 on 2025-03-29 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_favorites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='favorites',
        ),
    ]
