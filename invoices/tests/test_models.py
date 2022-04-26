from datetime import date
from django.test import TestCase
from model_mommy import mommy
from .. import models as invoice_models


class TestHelperFunctions(TestCase):
    """Test the helper functions."""

    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    file_name = "test_file.pdf"

    def test_invoice_upload_path(self):
        """Test the `invoice_upload_path` function."""
        invoice = mommy.make(
            invoice_models.Invoice,
            date_ordered=self.today,
            supplier__slug="test-supplier",
            order_number="123",
        )
        result = invoice_models.invoice_upload_path(
            instance=invoice,
            filename=self.file_name,
        )
        self.assertEqual(
            result,
            f"test-supplier/{self.today_str}/123-test_file.pdf",
        )

    def test_invoice_upload_path_no_order_num(self):
        """Test the `invoice_upload_path` function with no order number."""
        invoice = mommy.make(
            invoice_models.Invoice,
            date_ordered=self.today,
            supplier__slug="test-supplier",
            order_number=None,
        )
        result = invoice_models.invoice_upload_path(
            instance=invoice,
            filename=self.file_name,
        )
        self.assertEqual(
            result,
            f"test-supplier/{self.today_str}/test_file.pdf",
        )


class TestInvoice(TestCase):
    """Test the `Invoice` model."""

    def test_supplier_str(self):
        """Test the `__str__` method."""
        self.assertIsInstance(
            str(mommy.make(invoice_models.Invoice)),
            str,
        )

    def test_is_complete_false(self):
        """Test the `is_complete` method returns false when the invoice is not
        yet complete.
        """
        invoice = mommy.make(invoice_models.Invoice, date_added=None)
        self.assertFalse(invoice.is_complete)

    def test_is_complete_true(self):
        """Test the `is_complete` method returns true when the invoice is
        complete.
        """
        invoice = mommy.make(
            invoice_models.Invoice,
            date_added=date.today(),
            order_number="abc",
            subtotal=10,
            vat=5,
            delivery=5,
            promotion=5,
            total=15,
        )
        self.assertTrue(invoice.is_complete)


class TestInvoiceItem(TestCase):
    """Test the `InvoiceItem` model."""

    def test_supplier_str(self):
        """Test the `__str__` method."""
        self.assertIsInstance(
            str(mommy.make(invoice_models.InvoiceItem)),
            str,
        )

    def test_clean_promotion(self):
        """Test that thw `clean` method cleans the promotion value."""
        invoice = mommy.make(
            invoice_models.Invoice,
            subtotal=100,
            vat=20,
            delivery=10,
            promotion=10,
        )
        invoice.clean()
        self.assertEqual(invoice.promotion, -10)

        invoice = mommy.make(
            invoice_models.Invoice,
            subtotal=100,
            vat=20,
            delivery=10,
            promotion=-20,
        )
        invoice.clean()
        self.assertEqual(invoice.promotion, -20)
