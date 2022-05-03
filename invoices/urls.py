from django.urls import path
from . import views

app_name = "invoices"

urlpatterns = [
    path("", views.InvoiceUpload.as_view(), name="upload_new"),
    path(
        "<int:invoice_id>/edit/",
        views.InvoiceEdit.as_view(),
        name="invoice-edit",
    ),
]
