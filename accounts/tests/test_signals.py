from django.test import TestCase
from django.contrib.auth.models import User
from model_mommy import mommy


class TestOnNewUser(TestCase):
    """Test the on_new_user signal."""

    def test_new_std_user_staff(self):
        """When a new standard user is created, test that it is turned into a
        staff user.
        """
        user = mommy.make(User, is_superuser=False, is_staff=False)
        self.assertTrue(user.is_staff)

    def test_new_std_user_group(self):
        """When a new standard user is created, test that it is added to the
        "Standard Users" group.
        """
        user = mommy.make(User, is_superuser=False, is_staff=False)
        self.assertTrue(user.groups.filter(name="Standard Users").exists())

    def test_new_superuser(self):
        """When a new superuser is created, it should not do anything. We check
        this by checking that the user is not part of the "Standard Users"
        group.
        """
        user = mommy.make(User, is_superuser=True, is_staff=False)
        self.assertFalse(user.groups.filter(name="Standard Users").exists())

    def test_changes(self):
        """When an existing user is changed, check that no additional changes
        are made to that user. We'll test this by removing the group and
        removing the staff user privileges after creating the user.
        """
        user = mommy.make(User, is_superuser=False, is_staff=True)
        user.groups.clear()
        user.is_staff = False
        user.save()
        self.assertFalse(user.groups.filter(name="Standard Users").exists())
        self.assertFalse(user.is_staff)
