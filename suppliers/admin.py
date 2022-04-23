from django.contrib import admin
from . import models as supplier_models


@admin.register(supplier_models.Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "website"]
    search_fields = ["id", "name", "slug", "website"]
    ordering = ["name"]
    prepopulated_fields = {"slug": ["name"]}
