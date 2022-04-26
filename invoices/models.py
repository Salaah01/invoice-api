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
    date_str = (instance.date_ordered or instance.date_added).strftime(
        "%Y-%m-%d"
    )

    upload_path = f"{instance.supplier.slug}/{date_str}/"
    if instance.order_number:
        upload_path += f"{slugify(instance.order_number)}-"
    upload_path += f"{fname}{ext}"

    return upload_path


class Invoice(models.Model):
    """Represents an invoice item. Contains details on an invoice."""

    date_ordered = models.DateField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        verbose_name="Order/Invoice Number",
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    subtotal = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
    )
    vat = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
    )
    delivery = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
    )
    promotion = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
    )
    total = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
    )
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
        if (self.promotion or 0) > 0:
            self.promotion = -self.promotion
        super().clean()

    @property
    def is_complete(self) -> bool:
        """Returns True if the invoice is complete.

        :return: True if the invoice is complete.
        :rtype: bool
        """
        for field in (
            self.date_added,
            self.order_number,
            self.subtotal,
            self.vat,
            self.delivery,
            self.promotion,
            self.total,
        ):
            if field is None:
                return False
        else:
            return True


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
