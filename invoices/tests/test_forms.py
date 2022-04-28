from types import SimpleNamespace
from collections import namedtuple
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from model_mommy import mommy
from suppliers import models as supplier_models
from .. import forms as invoice_forms


mocked_parsed_data = SimpleNamespace(
    parse=lambda _1, _2: None,
    process_invoice=lambda: None,
    order_date="2020-01-01",
    order_number="12345",
    subtotal=0,
    vat=0,
    delivery=0,
    promotion=0,
    total=0,
)

_mocked_parser = {
    "parse": lambda _1, _2: None,
    "process_invoice": lambda: None,
    "order_date": "2020-01-01",
    "order_number": "12345",
    "subtotal": 0,
    "vat": 0,
    "delivery": 0,
    "promotion": 0,
    "total": 0,
}
mocked_parser = namedtuple("mocked_parser", _mocked_parser.keys())(
    **_mocked_parser
)


class MockedParser:
    order_date = "2020-01-01"
    order_number = "12345"
    subtotal = 0
    vat = 0
    delivery = 0
    promotion = 0
    total = 0

    def __init__(self, *args, **kwargs):
        return None

    def parse(self, *args, **kwargs) -> None:
        return None

    def process_invoice(self) -> None:
        return None


mocked_parser = MockedParser()


class InvoiceUploadFormTest(TestCase):
    """Unittests for the `InvoiceUpload` form."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        super().setUpTestData()
        cls.user = mommy.make(User)
        for _ in range(10):
            mommy.make(supplier_models.Supplier)
        cls.supplier = mommy.make(
            supplier_models.Supplier,
            name="Soak Rochford",
        )
        mommy.make(
            supplier_models.UserSupplier,
            user=cls.user,
            supplier=cls.supplier,
        )

    def test_supplier_choices(self):
        """That that the supplier choices have the correct options."""
        form = invoice_forms.InvoiceUpload(user=self.user)
        self.assertEqual(
            set(form.fields["supplier"].queryset.values_list("id", flat=True)),
            set(
                supplier_models.UserSupplier.choices(self.user).values_list(
                    "id",
                    flat=True,
                )
            ),
        )

    def test_save(self):
        """Test that the `save` method works."""
        file = SimpleUploadedFile(
            "test.pdf",
            b"file_content",
        )
        form = invoice_forms.InvoiceUpload(
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
