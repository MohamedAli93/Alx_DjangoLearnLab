from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Book
from django.db.utils import OperationalError

@receiver(post_migrate)
def create_groups_permissions(sender, **kwargs):
    if sender.name == "bookshelf":  # ✅ Ensures it only runs for this app
        try:
            content_type = ContentType.objects.get_for_model(Book)
            
            permissions = [
                Permission.objects.get_or_create(codename="can_view", name="Can view book", content_type=content_type),
                Permission.objects.get_or_create(codename="can_create", name="Can create book", content_type=content_type),
                Permission.objects.get_or_create(codename="can_edit", name="Can edit book", content_type=content_type),
                Permission.objects.get_or_create(codename="can_delete", name="Can delete book", content_type=content_type),
            ]

            groups = {
                "Viewers": ["can_view"],
                "Editors": ["can_view", "can_create", "can_edit"],
                "Admins": ["can_view", "can_create", "can_edit", "can_delete"],
            }

            for group_name, perms in groups.items():
                group, created = Group.objects.get_or_create(name=group_name)
                if created:
                    for perm_codename in perms:
                        perm = Permission.objects.get(codename=perm_codename)
                        group.permissions.add(perm)
        except OperationalError:
            print("Database tables are not ready yet. Skipping group/permission creation.")