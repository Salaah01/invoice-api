from django.contrib import admin
from . import models as invoice_models


class InvoiceItemInline(admin.TabularInline):
    model = invoice_models.InvoiceItem
    extra = 0


@admin.register(invoice_models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
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
        "is_complete",
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

    def is_complete(self, obj: invoice_models.Invoice) -> bool:
        """Returns True if the invoice is complete."""
        return obj.is_complete

    is_complete.boolean = True
