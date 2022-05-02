"""Sets the permissions for the standard user group."""

from django.db import migrations
from django.apps.registry import apps as global_apps


def default_group_permissions(apps, schema_editor):
    """Sets the permissions for the standard user group."""
    Group = apps.get_model("auth", "Group")
    group = Group.objects.get(name="Standard Users")

    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    # Content types with permissions.
    content_types_map = [
        ("suppliers", "supplier", ["add", "view"]),
        ("products", "product", ["add", "view"]),
        ("products", "productcategory", ["add", "view"]),
        ("invoices", "invoice", ["add", "view", "change", "delete"]),
        ("invoices", "invoiceitem", ["add", "view", "change", "delete"]),
    ]

    content_types = {}
    for app_label, model_name, permissions in content_types_map:
        content_type = ContentType.objects.get_for_model(
            global_apps.get_model(app_label, model_name)
        )
        content_types[content_type] = [
            f"{perm}_{model_name}" for perm in permissions
        ]

    # Add permissions
    for content_type, permissions in content_types.items():
        for permission in Permission.objects.filter(
            content_type=content_type, codename__in=permissions
        ):
            group.permissions.add(permission)


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0001_initial"),
        ("accounts", "0001_default_group"),
        ("suppliers", "0002_usersupplier"),
        ("products", "0001_initial"),
        ("invoices", "0004_invoice_user"),
    ]

    operations = [migrations.RunPython(default_group_permissions)]
