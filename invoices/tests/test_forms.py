from django.test import TestCase
from django.contrib.auth.models import User
from model_mommy import mommy
from suppliers import models as supplier_models
from .. import forms as invoice_forms, models as invoice_models


class InvoiceUploadFormTest(TestCase):
    """Unittests for the `InvoiceUpload` form."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        super().setUpTestData()
        cls.user = mommy.make(User)
        for _ in range(10):
            mommy.make(supplier_models.Supplier)
        cls.supplier_amazon = mommy.make(
            supplier_models.Supplier,
            name="Amazon",
        )
        mommy.make(
            supplier_models.UserSupplier,
            user=cls.user,
            supplier=cls.supplier_amazon,
        )

    def test_supplier_choices(self):
        """That that the supplier choices have the correct options."""
        form = invoice_forms.InvoiceUpload(user=self.user)
        self.assertEqual(
            set(form.fields["supplier"].queryset.values_list("id", flat=True)),
            set(
                supplier_models.UserSupplier.choices(self.user).values_list(
                    "id", flat=True
                )
            ),
        )
