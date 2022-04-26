from django.db import models
from django.contrib.auth.models import User
from parser.parse_for_supplier import SUPPLIER_PARSERS


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


class UserSupplier(models.Model):
    """Represents a user's association with a supplier."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_supplier"
        unique_together = ("user", "supplier")

    def __str__(self):
        return f"{self.user} - {self.supplier}"

    @classmethod
    def choices(cls, user: User) -> models.QuerySet["Supplier"]:
        """Returns a queryset of suppliers which include the user's suppliers
        excluding any suppliers not supported by the parser.
        """
        return Supplier.objects.filter(
            id__in=cls.objects.filter(
                user=user,
                supplier__name__in=SUPPLIER_PARSERS.keys(),
            ).values_list("supplier_id", flat=True)
        )
