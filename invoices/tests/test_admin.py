from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from model_mommy import mommy


class InvoiceAdminTest(TestCase):
    """Tests for the InvoiceAdmin class."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        super().setUpTestData()
        cls.superuser = User.objects.create_superuser(username="test_user")
        cls.std_user = mommy.make(User, is_staff=True)

    def test_changelist_superuser(self):
        """Test the change list for a superuser. It should return all the
        results.
        """
        client = Client()
        client.force_login(self.superuser)

        response = client.get(reverse("admin:invoices_invoice_changelist"))
        self.assertEqual(response.status_code, 200)
