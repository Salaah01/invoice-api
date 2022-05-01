from django.contrib import admin
from django.http import HttpRequest
from core.admin import PermModelAdmin
from . import models as invoice_models


class InvoiceItemInline(admin.TabularInline):
    model = invoice_models.InvoiceItem
    extra = 0


@admin.register(invoice_models.Invoice)
class InvoiceAdmin(PermModelAdmin):
    list_display = [
        "id",
        "date_ordered",
        "date_added",
        "order_number",
        "supplier",
        "subtotal",
        "vat",
        "delivery",
        "promotion",
        "total",
        "attachment",
        "completed",
    ]
    search_fields = [
        "id",
        "order_number",
        "supplier__name",
    ]
    list_filter = [
        "date_ordered",
        "date_added",
        "supplier",
    ]
    ordering = ["-date_ordered"]
    date_hierarchy = "date_ordered"
    inlines = [InvoiceItemInline]
