"""Tests for the `views` module."""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from model_mommy import mommy
from suppliers import models as supplier_models


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
