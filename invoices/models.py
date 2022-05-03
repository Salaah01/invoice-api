import typing as _t
import os
from django.db import models
from django.utils.text import slugify
from core import number_utils
from suppliers.models import Supplier
from products.models import Product, ProductCategory
from parser.parse_for_supplier import BaseSupplierParser


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

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
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
    completed = models.BooleanField(default=False)

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

    def update_parsed_data(self, parser: BaseSupplierParser):
        """Updates the invoice item with the parsed data from the parser.

        :param parser: The parser to use to parse the invoice item.
        :type parser: BaseSupplierParser
        """
        self.date_ordered = parser.order_date
        self.order_number = parser.order_number
        self.subtotal = parser.subtotal or 0
        self.vat = parser.vat or 0
        self.delivery = parser.delivery or 0
        self.promotion = parser.promotion or 0
        self.total = parser.total or 0

        self.save()

    def add_from_items_breakdown(self, items_breakdown: dict):
        """Adds invoice items from a dictionary of items.

        :param items_breakdown: The dictionary of items to add to the invoice.
        :type items_breakdown: dict
        """
        invoice_items = []
        for product_name, product_details in items_breakdown.items():
            invoice_items.append(
                self.add_item(
                    product_details.get("quantity"),
                    product_details.get("price_ex_vat"),
                    product_name=product_name,
                )
            )
        return invoice_items

    def add_item(
        self,
        quantity: int,
        price: float,
        product: _t.Optional[Product] = None,
        product_name: _t.Optional[str] = None,
    ) -> "InvoiceItem":
        """Adds an invoice item.

        :param quantity: The quantity of the item.
        :type quantity: int
        :param price: The price of the item.
        :type price: float
        :param product: The product to add to the invoice.
        :type product: Product
        :param product_name: The name of the product to add to the invoice.
        :type product_name: str
        :return: The invoice item that was added.
        :rtype: InvoiceItem
        """

        if product is None and product_name is None:
            raise ValueError(
                "Either product or product_name must be provided."
            )

        if product is None:
            product, _ = Product.objects.get_or_create(
                name=product_name,
                supplier=self.supplier,
            )

        invoice_item = InvoiceItem.objects.create(
            invoice=self,
            product=product,
            quantity=quantity,
            price_ex_vat=price,
            category=product.default_category,
        )
        invoice_item.save()
        return invoice_item


class InvoiceItem(models.Model):
    """Represents a single item on an invoice."""

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    price_ex_vat = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    @property
    def unit_price(self) -> float:
        """Returns the unit price of the invoice item."""
        return number_utils.float_to_dp(self.price_ex_vat / self.quantity)
