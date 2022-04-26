from django.urls import path
from . import views

app_name = "invoices"

urlpatterns = [
    path("", views.InvoiceUpload.as_view(), name="upload_new"),
]
