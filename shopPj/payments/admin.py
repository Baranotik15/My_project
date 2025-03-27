from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'payment_method',
        'status',
        'payment_date',
    )
    list_filter = (
        'status',
        'payment_method',
    )
    search_fields = (
        'order__id',
    )
    ordering = (
        '-payment_date',
    )
