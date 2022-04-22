import os
from django.db import models
from django.utils.text import slugify
from suppliers.models import Supplier
from products.models import Product


def invoice_upload_path(instance: "Invoice", filename: str) -> str:
    """Returns the path to the invoice file.

    :param instance: The invoice instance.
    :type instance: Invoice
    :param filename: The filename of the invoice.
    :type filename: str
    :return: The path to the invoice file in the format:
        `/<supplier_slug>/<date>/<invoice_number>-<filename>`
    :rtype: str
    """
    fname, ext = os.path.splitext(filename.lower())
    fname = slugify(fname)
    date_str = instance.date.strftime("%Y-%m-%d")

    upload_path = f"{instance.supplier.slug}/{date_str}"
    if instance.invoice_number:
        upload_path += f"/{slugify(instance.invoice_number)}-"
    upload_path += f"{fname}{ext}"

    return upload_path


class Invoice(models.Model):
    """Represents an invoice item. Contains details on an invoice."""

    date_ordered = models.DateField()
    date_added = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=32, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    subtotal = models.DecimalField(max_digits=7, decimal_places=2)
    vat = models.DecimalField(max_digits=7, decimal_places=2)
    delivery = models.DecimalField(max_digits=7, decimal_places=2)
    promotion = models.DecimalField(max_digits=7, decimal_places=2)
    total = models.DecimalField(max_digits=7, decimal_places=2)
    attachment = models.FileField(
        upload_to=invoice_upload_path,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "invoice"
        ordering = ["-date_ordered"]

    def __str__(self):
        return f"{self.supplier.name} - {self.date_ordered}"

    def clean(self):
        """Ensure that the promotion value is negative."""
        if self.promotion > 0:
            self.promotion = -self.promotion
        super().clean()


class InvoiceItem(models.Model):
    """Represents a single item on an invoice."""

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="products",
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_ex_vat = models.DecimalField(max_digits=7, decimal_places=2)
