from django.db import models


class Supplier(models.Model):
    """Represents a supplier."""

    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=32, unique=True)
    website = models.URLField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = "supplier"
        ordering = ["name"]

    def __str__(self):
        return self.name
