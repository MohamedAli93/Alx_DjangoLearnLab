from django.contrib import admin
from .models import Book
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'date_of_birth', 'profile_photo', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'date_of_birth']
    search_fields = ['username', 'email']
    ordering = ['username']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'created_by')
    search_fields = ('title', 'author', 'publication_year')
    list_filter = ("author", "publication_year")
admin.site.register(Book, BookAdmin)
# Register your models here.

# Define Groups and Assign Permissions
def setup_permissions():
    # Get Content Type for Book Model
    content_type = ContentType.objects.get_for_model(Book)

    # Define Permissions
    permissions = {
        "can_view": Permission.objects.get(codename="can_view", content_type=content_type),
        "can_create": Permission.objects.get(codename="can_create", content_type=content_type),
        "can_edit": Permission.objects.get(codename="can_edit", content_type=content_type),
        "can_delete": Permission.objects.get(codename="can_delete", content_type=content_type),
    }

    # Create Groups and Assign Permissions
    groups_permissions = {
        "Viewers": ["can_view"],
        "Editors": ["can_view", "can_edit", "can_create"],
        "Admins": ["can_view", "can_edit", "can_create", "can_delete"]
    }

    for group_name, perms in groups_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            for perm in perms:
                group.permissions.add(permissions[perm])

# Run setup_permissions after migrations
setup_permissions()