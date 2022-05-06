from django.test import TestCase
from model_bakery import baker
from .. import models as product_models


class TestProductCategory(TestCase):
    """Test the `ProductCategory` model."""

    def test_supplier_str(self):
        """Test the `__str__` method."""
        self.assertIsInstance(
            str(baker.make(product_models.ProductCategory)),
            str,
        )


class TestProduct(TestCase):
    """Test the `Product` model."""

    def test_str(self):
        """Test the `__str__` method."""
        self.assertIsInstance(
            str(baker.make(product_models.Product, name="Test Product")),
            str,
        )

    def test_long_str(self):
        """Test the `__str__` method with a long name."""
        self.assertIsInstance(
            str(baker.make(product_models.Product, name="T" * 100)),
            str,
        )

    def test_save(self):
        """Test the `save` method where all fields are entered."""
        product = baker.make(
            product_models.Product,
            name="Test Product",
            slug="test-product",
        )
        self.assertIsInstance(product, product_models.Product)

    def test_save_no_slug(self):
        """Test the `save` method where no slug is entered. It should
        automatically create a slug.
        """
        product = baker.make(
            product_models.Product,
            name="Test Product",
        )
        self.assertIsInstance(product, product_models.Product)
        self.assertIsNotNone(product.slug)
