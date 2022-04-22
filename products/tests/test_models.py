from django.test import TestCase
from model_mommy import mommy
from .. import models as product_models


class TestProductCategory(TestCase):
    """Test the `ProductCategory` model."""

    def test_supplier_str(self):
        """Test the `__str__` method."""
        self.assertIsInstance(
            str(mommy.make(product_models.ProductCategory)),
            str,
        )


class TestProduct(TestCase):
    """Test the `Product` model."""

    def test_supplier_str(self):
        """Test the `__str__` method."""
        self.assertIsInstance(
            str(mommy.make(product_models.Product)),
            str,
        )
