"""Contains a collection of generic model choices."""

from django.db import models


class UnitChoices(models.TextChoices):
    """Represents the various units of measurement."""

    KILOGRAM = "kg", "kg"
    GRAM = "g", "g"
    MILLIGRAM = "mg", "mg"
    LITRE = "l", "l"
    MILLILITRE = "ml", "ml"
    PIECE = "pcs", "pcs"
