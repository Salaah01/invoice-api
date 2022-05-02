"""Migration to create a new group for all standard users."""

from django.db import migrations


def new_group(apps, schema_editor):
    """Create a new group."""
    Group = apps.get_model("auth", "Group")
    Group.objects.create(name="Standard Users")


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [migrations.RunPython(new_group)]
