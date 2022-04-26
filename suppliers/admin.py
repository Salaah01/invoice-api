from django.contrib import admin
from . import models as supplier_models


@admin.register(supplier_models.Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "website"]
    search_fields = ["id", "name", "slug", "website"]
    ordering = ["name"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(supplier_models.UserSupplier)
class UserSupplierAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "supplier"]
    search_fields = [
        "id",
        "user__username",
        "user__email",
        "supplier__name",
        "supplier__website",
    ]
    ordering = ["user", "supplier"]
    raw_id_fields = ["user", "supplier"]
    list_filter = ["supplier"]
