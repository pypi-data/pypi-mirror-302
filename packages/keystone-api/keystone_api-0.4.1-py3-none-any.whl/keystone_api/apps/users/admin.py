"""Extends the builtin Django admin interface for the parent application.

Extends and customizes the site-wide administration utility with
interfaces for managing application database constructs.
"""

import django.contrib.auth.admin
from django.conf import settings
from django.contrib import admin, auth

from .models import *

settings.JAZZMIN_SETTINGS['icons'].update({
    'users.User': 'fa fa-user',
    'users.ResearchGroup': 'fa fa-users',
})

settings.JAZZMIN_SETTINGS['order_with_respect_to'].extend([
    'users.User', 'users.ResearchGroup'
])


@admin.register(User)
class UserAdmin(auth.admin.UserAdmin):
    """Admin interface for managing user accounts."""

    @admin.action
    def activate_selected_users(self, request, queryset) -> None:
        """Mark selected users as active."""

        queryset.update(is_active=True)

    @admin.action
    def deactivate_selected_users(self, request, queryset) -> None:
        """Mark selected users as inactive."""

        queryset.update(is_active=False)

    readonly_fields = ("last_login", "date_joined", "is_ldap_user")
    actions = [activate_selected_users, deactivate_selected_users]
    fieldsets = (
        ("User Info", {"fields": ("first_name", "last_name", "email", "department", "role", "last_login", "date_joined", 'is_ldap_user')}),
        ("Credentials", {"fields": ("username", "password")}),
        ("Permissions",
         {"fields": (
             "is_active",
             "is_staff",
             "is_superuser",
         )})
    )


@admin.register(ResearchGroup)
class ResearchGroupAdmin(admin.ModelAdmin):
    """Admin interface for managing research group delegates."""

    @staticmethod
    @admin.display
    def pi(obj: ResearchGroup) -> str:
        """Return the username of the research group PI."""

        return obj.pi.username

    pi.admin_order_field = 'pi__username'

    list_display = ['name', pi]
    filter_horizontal = ('admins', 'members')
    ordering = ['name', ]
    search_fields = ['name', 'pi__username']
