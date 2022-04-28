from django.test import TestCase
from django.contrib.auth.models import User
from model_mommy import mommy
from .. import admin as invoice_admin, models as invoice_models


class InvoiceAdminTest(TestCase):
    """Tests for the InvoiceAdmin class."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        super().setUpTestData()
        cls.superuser = User.objects.create_superuser(
            username="test_user",
        )

    # def test_is_complete(self):
    #     """Test the `is_complete` method."""
    #     invoice = mommy.make(invoice_models.Invoice)
    #     self.assertEqual(
    #         invoice_admin.InvoiceAdmin.is_complete(None, invoice),
    #         invoice.is_complete,
    #     )
