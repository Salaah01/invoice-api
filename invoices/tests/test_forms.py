import os
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from suppliers import models as supplier_models
from .. import forms as invoice_forms, models as invoice_models


class InvoiceUploadFormTest(TestCase):
    """Unittests for the `InvoiceUpload` form."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        super().setUpTestData()
        cls.user = baker.make(User)
        for _ in range(10):
            baker.make(supplier_models.Supplier)
        cls.supplier = baker.make(
            supplier_models.Supplier,
            name="Soak Rochford",
        )
        baker.make(
            supplier_models.UserSupplier,
            user=cls.user,
            supplier=cls.supplier,
        )

    def test_supplier_choices(self):
        """That that the supplier choices have the correct options."""
        form = invoice_forms.InvoiceUploadForm(user=self.user)
        self.assertEqual(
            set(form.fields["supplier"].queryset.values_list("id", flat=True)),
            set(
                supplier_models.UserSupplier.choices(self.user).values_list(
                    "id",
                    flat=True,
                )
            ),
        )

    def test_save_no_invoice(self):
        """Test that the `save` method works. In this test, an actual invoice
        is not attached to the form.
        """
        file = SimpleUploadedFile(
            "test.pdf",
            b"file_content",
        )
        form = invoice_forms.InvoiceUploadForm(
            user=self.user,
            data={
                "supplier": self.supplier.id,
                "attachment": file,
            },
            files={"attachment": file},
        )

        self.assertTrue(form.is_valid(), form.errors)
        invoice = form.save()
        self.assertEqual(invoice.supplier, self.supplier)
        self.assertEqual(invoice.user, self.user)

    def test_save_with_invoice(self):
        """Test that the `save` method works. In this test, an actual invoice
        is used, so it is expected that the invoice is parsed.
        """
        invoice_fp = os.path.join(
            "invoices",
            "tests",
            "soak_rochford_invoice.pdf",
        )
        file = SimpleUploadedFile(
            "test.pdf",
            open(invoice_fp, "rb").read(),
        )
        form = invoice_forms.InvoiceUploadForm(
            user=self.user,
            data={
                "supplier": self.supplier.id,
                "attachment": file,
            },
            files={"attachment": file},
        )

        self.assertTrue(form.is_valid(), form.errors)
        invoice = form.save()
        self.assertEqual(invoice.supplier, self.supplier)


class InvoiceFormTest(TestCase):
    """Tests for the `invoice_item_formset` function."""

    def test_formset_no_initial(self):
        """Test that the formset is created without initial data."""
        formset = invoice_forms.invoice_item_formset(
            invoice_items=invoice_models.InvoiceItem.objects.none(),
        )
        self.assertEqual(len(formset), 0)

    def test_formset_with_initial(self):
        """Test that the formset is created with initial data."""
        baker.make(invoice_models.InvoiceItem)
        formset = invoice_forms.invoice_item_formset(
            invoice_items=invoice_models.InvoiceItem.objects.all(),
        )
        self.assertEqual(len(formset), 1)
