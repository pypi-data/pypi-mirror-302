"""Custom permission objects used to manage access to HTTP endpoints.

Permission classes control access to API resources by determining user
privileges for different HTTP operations. They are applied at the view level,
enabling authentication and authorization to secure endpoints based on
predefined access rules.
"""

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View

from .models import *

__all__ = ['IsGroupAdminOrReadOnly', 'IsSelfOrReadOnly']


class IsGroupAdminOrReadOnly(permissions.BasePermission):
    """Grant read-only access to all authenticated users.

    Staff users retain all read/write permissions.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        """Return whether the request has permissions to access the requested resource."""

        if request.method == 'TRACE':
            return request.user.is_staff

        return True

    def has_object_permission(self, request: Request, view: View, obj: ResearchGroup):
        """Return whether the incoming HTTP request has permission to access a database record."""

        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Update permissions are only allowed for staff and research group admins
        return request.user.is_staff or request.user in obj.get_privileged_members()


class IsSelfOrReadOnly(permissions.BasePermission):
    """Grant read-only permissions to everyone and limit write access to staff and record owners."""

    def has_permission(self, request: Request, view: View) -> bool:
        """Return whether the request has permissions to access the requested resource."""

        # Allow all users to read/update existing records
        # Rely on object level permissions for further refinement of update permissions
        if request.method in permissions.SAFE_METHODS or request.method in ('PUT', 'PATCH'):
            return True

        # Record creation/deletion is allowed for staff
        return request.user.is_staff

    def has_object_permission(self, request: Request, view: View, obj: User) -> bool:
        """Return whether the incoming HTTP request has permission to access a database record."""

        # Write operations are restricted to staff and user's modifying their own data
        is_record_owner = obj == request.user
        is_readonly = request.method in permissions.SAFE_METHODS
        return is_readonly or is_record_owner or request.user.is_staff
