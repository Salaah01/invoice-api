from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet


class PermModelAdmin(admin.ModelAdmin):
    """A model form where the user has access to certain features and data
    based on their user.
    """

    # The field which holds the user.
    user_id_field: str = "user_id"

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """Get the queryset for the model.

        :param request: The request.
        :type request: HttpRequest
        :return: The queryset.
        :rtype: QuerySet
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(**{self.user_id_field: request.user.id})
