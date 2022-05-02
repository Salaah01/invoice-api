from django.contrib import admin
from . import models as product_models


@admin.register(product_models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(product_models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "default_category", "supplier")
    search_fields = ("id", "name", "default_category__name", "supplier__name")
    list_filter = ("default_category", "supplier")
