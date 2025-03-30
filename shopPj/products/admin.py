from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "stock",
        "category",
        "created_at",
    )
    list_filter = (
        "category",
        "price",
    )
    search_fields = (
        "name",
        "category__name",
    )
    ordering = ("-created_at",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
