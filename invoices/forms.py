from django import forms
from suppliers import models as supplier_models
from . import models as invoice_models


class InvoiceUpload(forms.ModelForm):
    """Form captures a newly uploaded invoice along with some information to
    help parse the form.
    """

    supplier = forms.ModelChoiceField(supplier_models.Supplier.objects.none())

    class Meta:
        model = invoice_models.Invoice
        fields = ["supplier", "attachment"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields[
            "supplier"
        ].queryset = supplier_models.UserSupplier.choices(user)
