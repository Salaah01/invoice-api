from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.http import HttpRequest, HttpResponse
from . import forms


class InvoiceUpload(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request,
            "invoices/upload_new.html",
            {"form": forms.InvoiceUpload(user=request.user)},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form = forms.InvoiceUpload(
            request.POST,
            request.FILES,
            user=request.user,
        )
        if form.is_valid():
            form.save()
            return HttpResponse("OK")
        else:
            messages.error(request, form.errors)
            print(form.errors)
            return redirect("invoices:upload_new")
