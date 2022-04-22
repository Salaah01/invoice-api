from django.test import TestCase
from model_mommy import mommy
from .. import models as supplier_models


class TestSupplier(TestCase):
    """Test the `Supplier` model."""

    def test_supplier_str(self):
        """Test the `__str__` method."""
        self.assertIsInstance(str(mommy.make(supplier_models.Supplier)), str)
