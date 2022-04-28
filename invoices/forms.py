from django import forms
from django.contrib.auth.models import User
from suppliers import models as supplier_models
from parser import parse_for_supplier
from . import models as invoice_models


class InvoiceUpload(forms.ModelForm):
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

        try:
            parsed_data = parse_for_supplier.parse(
                invoice.attachment.file.name,
                invoice.supplier.name,
            )
            parsed_data.process_invoice()
        except Exception as e:
            # TODO: Log the error
            print("\033[91mErrors:\n" + str(e) + "\033[0m")
            return invoice

        invoice.date_ordered = parsed_data.order_date
        invoice.order_number = parsed_data.order_number
        invoice.subtotal = parsed_data.subtotal or 0
        invoice.vat = parsed_data.vat or 0
        invoice.delivery = parsed_data.delivery or 0
        invoice.promotion = parsed_data.promotion or 0
        invoice.total = parsed_data.total or 0
        invoice.save()
        return invoice
