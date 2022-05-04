from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from . import forms as invoice_forms, models as invoice_models


def with_invoice(func):
    """Decorator to ensure that the invoice is passed to view."""

    @wraps(func)
    def wrapper(request, invoice_id, *args, **kwargs):
        invoice = get_object_or_404(invoice_models.Invoice, pk=invoice_id)
        user = request.user
        if not user.is_authenticated:
            raise Http404("You must be logged in to view this page.")
        if user.has_perm("view_invoice", invoice) or invoice.user == user:
            return func(request, invoice, *args, **kwargs)
        raise Http404("This invoice does not exist or you do not have access.")

    return wrapper


class InvoiceUpload(View):
    """View where users are able to upload invoices."""

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request,
            "invoices/upload_new.html",
            {"form": invoice_forms.InvoiceUploadForm(user=request.user)},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form = invoice_forms.InvoiceUploadForm(
            request.POST,
            request.FILES,
            user=request.user,
        )
        if form.is_valid():
            form.save()
            return HttpResponse("OK")
        else:
            messages.error(request, form.errors)
            return redirect("invoices:upload_new")


@method_decorator(with_invoice, name="dispatch")
class InvoiceEdit(View):
    """View where users are able to edit the invoice and the invoice items."""

    def get(
        self,
        request: HttpRequest,
        invoice: invoice_models.Invoice,
    ) -> HttpResponse:
        invoice_form = invoice_forms.InvoiceForm(instance=invoice)
        invoice_items_formset = invoice_forms.invoice_item_formset(
            invoice.items.all()
        )

        return render(
            request,
            "invoices/edit.html",
            {
                "invoice_form": invoice_form,
                "invoice_items_formset": invoice_items_formset,
            },
        )
