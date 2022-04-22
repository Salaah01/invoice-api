from django.db import models
from suppliers.models import Supplier


class ProductCategory(models.Model):
    """Represents the various categories of products."""

    name = models.CharField(max_length=32, unique=True)

    class Meta:
        db_table = "product_category"
        ordering = ["name"]


class Product(models.Model):
    """Represents a product that can be purchased from a supplier."""

    name = models.CharField(max_length=100)
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="products",
    )
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)

    class Meta:
        db_table = "product"
        ordering = ["name"]
        unique_together = ["name", "supplier"]
