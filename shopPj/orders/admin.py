from django.contrib import admin
from django.db.models import F, Sum
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
        'total_price',
        'created_at',
    )
    list_filter = (
        'status',
    )
    search_fields = (
        'id',
        'user__username',
    )
    ordering = (
        '-created_at',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            total_price=Sum(
                F('order_items__quantity') * F('order_items__product__price')
            )
        )

    def total_price(self, obj):
        return obj.total_price or 0

    total_price.admin_order_field = 'total_price'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'product',
        'quantity',
    )
    list_filter = (
        'order',
    )
    search_fields = (
        'order__id',
        'product__name',
    )