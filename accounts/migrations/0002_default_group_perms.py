"""Migration to create a new group for all standard users."""

from django.db import migrations
from django.apps.registry import apps as global_apps


def default_group_permissions(apps, schema_editor):
    """Create a new group."""
    Group = apps.get_model("auth", "Group")
    group = Group.objects.get(name="Standard Users")

    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    # Content Types
    content_types_map = [
        ("suppliers", "supplier"),
        ("products", "product"),
        ("products", "productcategory"),
        ("invoices", "invoice"),
        ("invoices", "invoiceitem"),
    ]

    content_types = []
    for app_label, model_name in content_types_map:
        content_type = ContentType.objects.get_for_model(
            global_apps.get_model(app_label, model_name)
        )
        content_types.append(content_type)

    # Add permissions
    for content_type in content_types:
        for permission in Permission.objects.filter(content_type=content_type):
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
