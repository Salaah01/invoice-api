from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from model_bakery import baker
from .. import models as supplier_models


class TestSupplier(TestCase):
    """Test the `Supplier` model."""

    def test_supplier_str(self):
        """Test the `__str__` method."""
        self.assertIsInstance(str(baker.make(supplier_models.Supplier)), str)


class TestUserSupplier(TestCase):
    """Test the `UserSupplier` model."""

    def test_user_supplier_str(self):
        """Test the `__str__` method."""
        self.assertIsInstance(
            str(baker.make(supplier_models.UserSupplier)), str
        )

    @patch("suppliers.models.SUPPLIER_PARSERS", {"s1": 1, "s2": 2, "s3": 3})
    def test_choices(self):
        """Test the `choices` method."""
        user = baker.make(User)
        supplier_1 = baker.make(supplier_models.Supplier, name="s1")
        supplier_2 = baker.make(supplier_models.Supplier, name="s2")
        baker.make(supplier_models.Supplier, name="s3")
        baker.make(
            supplier_models.UserSupplier,
            user=user,
            supplier=supplier_1,
        )
        baker.make(
            supplier_models.UserSupplier,
            user=user,
            supplier=supplier_2,
        )
        self.assertEqual(
            set(
                supplier_models.UserSupplier.choices(user).values_list(
                    "name", flat=True
                )
            ),
            {"s1", "s2"},
        )
