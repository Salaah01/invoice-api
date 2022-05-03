from django import forms
from django.db.models import QuerySet
from django.contrib.auth.models import User
from suppliers import models as supplier_models
from parser import parse_for_supplier
from parser.parse_for_supplier import BaseSupplierParser
from . import models as invoice_models


class InvoiceUploadForm(forms.ModelForm):
    """Form captures a newly uploaded invoice along with some information to
    help parse the form.
    """

    supplier = forms.ModelChoiceField(supplier_models.Supplier.objects.none())
    # We won't use this field explicitly, but we need to define it to make the
    # `user` field accessible.
    user = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = invoice_models.Invoice
        fields = ["supplier", "attachment", "user"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields[
            "supplier"
        ].queryset = supplier_models.UserSupplier.choices(self.user)

    def clean_user(self) -> User:
        """Overrides the default `clean_user` method to return the user
        associated with the form.
        """
        return self.user

    def save(self, *args, **kwargs):
        """Save the invoice and attempt to parse it."""
        # Need to attach user to the invoice before saving.
        invoice = super().save(*args, **kwargs)
        parsed_data = self.parse_data(invoice)
        if parsed_data is None:
            return invoice

        invoice.save()
        invoice.update_parsed_data(parsed_data)
        invoice.add_from_items_breakdown(parsed_data.items_breakdown)

        return invoice

    @staticmethod
    def parse_data(invoice: invoice_models.Invoice) -> BaseSupplierParser:
        """Parse the invoice data and return the processed object.

        :param invoice: The invoice to parse
        :type invoice: invoice_models.Invoice
        :return: A supplier parser object
        :rtype: BaseSupplierParser
        """
        try:
            parsed_data = parse_for_supplier.parse(
                invoice.attachment.file.name,
                invoice.supplier.name,
            )
            parsed_data.process_invoice()
            return parsed_data
        except Exception as e:
            print("\033[91mErrors:\n" + str(e) + "\033[0m")
            return None


class InvoiceForm(forms.ModelForm):
    """Form to edit an invoice."""

    class Meta:
        model = invoice_models.Invoice
        fields = [
            "date_ordered",
            "order_number",
            "supplier",
            "subtotal",
            "vat",
            "delivery",
            "promotion",
            "total",
            "attachment",
        ]


class InvoiceItemForm(forms.ModelForm):
    """Form to edit an invoice item."""

    class Meta:
        model = invoice_models.InvoiceItem
        fields = [
            "product",
            "quantity",
            "price_ex_vat",
            "category",
        ]


def invoice_item_formset(
    invoice_items: QuerySet[invoice_models.InvoiceItem],
    **kwargs,
) -> forms.BaseInlineFormSet:
    """Returns a formset for invoice items.

    :param invoice_items: The invoice items to include in the formset.
    :type invoice_items: QuerySet[InvoiceItem]
    :param kwargs: Keyword arguments to pass to the formset.
    :type kwargs: dict
    :return: The formset for invoice items.
    :rtype: forms.BaseInlineFormSet
    """
    invoice_items_values = invoice_items.values(
        "product",
        "quantity",
        "price_ex_vat",
        "category",
    )

    extra = kwargs.pop("extra", len(invoice_items_values))

    formset = forms.inlineformset_factory(
        invoice_models.Invoice,
        invoice_models.InvoiceItem,
        form=InvoiceItemForm,
        extra=extra,
        **kwargs,
    )()

    for subform, invoice_item in zip(formset.forms, invoice_items_values):
        subform.initial = invoice_item

    return formset
