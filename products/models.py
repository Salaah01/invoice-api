from django.db import models
from suppliers import models as supplier_models


class ProductCategory(models.Model):
    """Represents the various categories of products."""

    name = models.CharField(max_length=32, unique=True)

    class Meta:
        db_table = "product_category"
        ordering = ["name"]


class Product(models.Model):
    """Represents a product that can be purchased from a supplier."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    supplier = models.ForeignKey(
        supplier_models.Supplier,
        on_delete=models.PROTECT,
        related_name="products",
    )
    default_category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="This value will be set automatically and updated "
        "periodically.",
    )

    class Meta:
        db_table = "product"
        ordering = ["name"]
        unique_together = ["slug", "supplier"]
