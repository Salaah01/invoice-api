from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group


@receiver(post_save, sender=User)
def on_new_user(sender, instance: User, created: bool, **kwargs):
    """When a new user is created, add the user to the "Standard Users" group
    and make them a staff user.
    """
    if not created:
        return
    if instance.is_superuser:
        return
    instance.is_staff = True
    instance.save()
    Group.objects.get(name="Standard Users").user_set.add(instance)
