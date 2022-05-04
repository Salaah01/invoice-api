"""Tests for the `views` module."""

from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from model_mommy import mommy
from suppliers import models as supplier_models
from .. import models as invoice_models


class BaseTestCase(TestCase):
    """Base test class for all tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        super().setUpTestData()
        cls.super_user = mommy.make(User, is_superuser=True)
        cls.supplier = mommy.make(
            supplier_models.Supplier,
            name="Soak Rochford",
        )
        mommy.make(
            supplier_models.UserSupplier,
            user=cls.super_user,
            supplier=cls.supplier,
        )

    def setUp(self):
        """Set up the test."""
        self.client = Client()
        self.client.force_login(self.super_user)

    def get_request(self, path: str = "/") -> HttpRequest:
        """Return the request object of the client."""
        return self.client.get(path).wsgi_request


class TestWithInvoice(BaseTestCase):
    """Test the `with_invoice` decorator."""

    def setUp(self):
        """Set up the test."""
        super().setUp()
        self.invoice = mommy.make(
            invoice_models.Invoice,
            supplier=self.supplier,
        )

    def test_with_invoice_superuser(self):
        """Test that the view is accessible to superusers."""
        res = self.client.get(
            reverse("invoices:invoice-edit", args=[self.invoice.id])
        )
        self.assertEqual(res.status_code, 200)

    def test_with_unauthenticated_user(self):
        """Test that the view is not accessible to unauthenticated users."""
        self.client.logout()
        res = self.client.get(
            reverse("invoices:invoice-edit", args=[self.invoice.id])
        )
        self.assertEqual(res.status_code, 404)

    def test_with_users_invoice(self):
        """Test that the view is accessible to the user who owns the invoice."""
        user = mommy.make(User)
        invoice = mommy.make(
            invoice_models.Invoice,
            user=user,
        )
        self.client.force_login(user)
        res = self.client.get(
            reverse("invoices:invoice-edit", args=[invoice.id])
        )
        self.assertEqual(res.status_code, 200)

    def test_with_unauthorised_user(self):
        """Test that the view is not accessible to a user who does not own the
        invoice.
        """
        user = mommy.make(User)
        self.client.force_login(user)
        res = self.client.get(
            reverse("invoices:invoice-edit", args=[self.invoice.id])
        )
        self.assertEqual(res.status_code, 404)

    def test_non_existant_invoice(self):
        """Test the GET request for a non-existant invoice."""
        res = self.client.get(
            reverse("invoices:invoice-edit", args=[self.invoice.id + 1])
        )
        self.assertEqual(res.status_code, 404)


class TestInvoice(BaseTestCase):
    """Tests for the `Invoice` view."""

    def test_get(self):
        """Test the GET request."""
        response = self.client.get(reverse("invoices:upload_new"))
        self.assertEqual(response.status_code, 200)

    def test_post_invalid_form(self):
        """Test the POST request with an invalid form."""
        response = self.client.post(
            reverse("invoices:upload_new"),
            data={"supplier": "", "attachment": ""},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("invoices:upload_new"))

    def test_post_valid_form(self):
        """Test the POST request with a valid form."""
        response = self.client.post(
            reverse("invoices:upload_new"),
            data={
                "supplier": self.supplier.id,
            },
            files={
                "attachment": SimpleUploadedFile("test.pdf", b"file_content")
            },
        )
        self.assertEqual(response.status_code, 200)
