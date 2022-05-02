from types import SimpleNamespace
from django.test import TestCase, Client
from django.contrib.auth.models import User
from model_mommy import mommy
from core import admin as core_admin
from invoices import models as invoice_models


class TestPermModelAdmin(TestCase):
    """Unittests for the `PermModelAdmin` class."""

    @classmethod
    def setUpTestData(cls):
        cls.std_user = mommy.make(User, is_staff=True)
        cls.superuser = mommy.make(User, is_superuser=True, is_staff=True)
        cls.invoice_1 = mommy.make(invoice_models.Invoice, user=cls.std_user)
        cls.invoice_2 = mommy.make(invoice_models.Invoice, user=cls.std_user)

        for _ in range(3):
            mommy.make(invoice_models.Invoice)

    def setUp(self):
        self.client = Client()

    def superuser_request(self) -> SimpleNamespace:
        """A mock object that imitates part of a request object for a
        superuser.
        """
        return SimpleNamespace(user=self.superuser, ordering=None)

    def std_user_request(self) -> SimpleNamespace:
        """A mock object that imitates part of a request object for a
        standard user.
        """
        return SimpleNamespace(user=self.std_user, ordering=None)

    def test_get_queryset_superuser(self):
        """Test the `get_queryset` method for a superuser. It should return all
        the results.
        """
        qs = core_admin.PermModelAdmin(
            invoice_models.Invoice, None
        ).get_queryset(
            self.superuser_request(),
        )
        self.assertEqual(qs.count(), 5)

    def test_get_queryset_std_user(self):
        """Test the `get_queryset` method for a standard user. It should
        return only the results for the user.
        """
        qs = core_admin.PermModelAdmin(
            invoice_models.Invoice, None
        ).get_queryset(
            self.std_user_request(),
        )
        self.assertEqual(qs.count(), 2)
