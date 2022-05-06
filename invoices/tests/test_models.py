from datetime import date
from django.test import TestCase
from model_bakery import baker
from products import models as product_models
from .. import models as invoice_models


class TestHelperFunctions(TestCase):
    """Test the helper functions."""

    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    file_name = "test_file.pdf"

    def test_invoice_upload_path(self):
        """Test the `invoice_upload_path` function."""
        invoice = baker.make(
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
        invoice = baker.make(
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

    def test_str(self):
        """Test the `__str__` method."""
        self.assertIsInstance(
            str(baker.make(invoice_models.Invoice)),
            str,
        )

    def test_clean_promotion(self):
        """Test that the `clean` method cleans the promotion value."""
        invoice = baker.make(
            invoice_models.Invoice,
            subtotal=100,
            vat=20,
            delivery=10,
            promotion=10,
        )
        invoice.clean()
        self.assertEqual(invoice.promotion, -10)

        invoice = baker.make(
            invoice_models.Invoice,
            subtotal=100,
            vat=20,
            delivery=10,
            promotion=-20,
        )
        invoice.clean()
        self.assertEqual(invoice.promotion, -20)

    def test_add_item_product(self):
        """Test that the `add_item` adds an invoice item correctly when a
        product is provided.
        """
        product = baker.make(product_models.Product)
        invoice = baker.make(invoice_models.Invoice)
        invoice_item = invoice.add_item(1, 10, product)

        self.assertEqual(invoice_item.product, product)
        self.assertEqual(invoice_item.quantity, 1)
        self.assertEqual(invoice_item.price_ex_vat, 10)

    def test_add_item_product_name(self):
        """Test that the `add_item` adds an invoice item correctly when a
        product name is provided.
        """
        invoice = baker.make(invoice_models.Invoice)
        invoice_item = invoice.add_item(1, 10, product_name="Test Product")

        self.assertEqual(invoice_item.product.name, "Test Product")
        self.assertEqual(invoice_item.quantity, 1)
        self.assertEqual(invoice_item.price_ex_vat, 10)

    def test_add_item_no_product(self):
        """Test that the `add_item` raises an error when no product nor
        product_name is provided.
        """
        invoice = baker.make(invoice_models.Invoice)
        with self.assertRaises(ValueError):
            invoice.add_item(1, 10)


class TestInvoiceItem(TestCase):
    """Test the `InvoiceItem` model."""

    def test_str(self):
        """Test the `__str__` method."""
        self.assertIsInstance(
            str(baker.make(invoice_models.InvoiceItem)),
            str,
        )

    def test_unit_price(self):
        """Test the `unit_price` property."""
        item = baker.make(
            invoice_models.InvoiceItem,
            quantity=2,
            price_ex_vat=10,
        )
        self.assertEqual(item.unit_price, 5)
