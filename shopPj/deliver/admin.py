from django.contrib import admin
from .models import Deliver


@admin.register(Deliver)
class DeliverAdmin(admin.ModelAdmin):
    date_hierarchy = "start_time"
    list_display = (
        "order",
        "deliver_method",
        "status",
        "start_time",
        "finish_time",
        "tracking_number",
    )
    list_filter = ("status", "deliver_method")
    search_fields = ("order__id", "tracking_number", "address")
    ordering = ("-start_time",)
