from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "image",
    )
    list_editable = (
        "name",
        "image",
    )
    fields = (
        "name",
        "image",
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
        "image"
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
    list_editable = (
        "name",
        "price",
        "stock",
        "category",
        "image",
    )
    fields = (
        "name",
        "price",
        "stock",
        "category",
        "image",
    )

    actions = ['delete_selected']


    def delete_selected(self, request, queryset):
        queryset.delete()

    delete_selected.short_description = "Удалить выбранные товары"

