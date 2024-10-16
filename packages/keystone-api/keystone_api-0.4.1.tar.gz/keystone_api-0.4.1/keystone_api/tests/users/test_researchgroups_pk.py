"""Function tests for the `/users/researchgroups/<pk>/` endpoint."""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User
from tests.utils import CustomAsserts


class EndpointPermissions(APITestCase, CustomAsserts):
    """Test endpoint user permissions.

    Permissions depend on whether the user is a member of the record's associated research group.

    Endpoint permissions are tested against the following matrix of HTTP responses.

    | Authentication               | GET | HEAD | OPTIONS | POST | PUT | PATCH | DELETE | TRACE |
    |------------------------------|-----|------|---------|------|-----|-------|--------|-------|
    | Anonymous user               | 403 | 403  | 403     | 403  | 403 | 403   | 403    | 403   |
    | Nonmember accessing group    | 200 | 200  | 200     | 405  | 403 | 403   | 403    | 403   |
    | Group member accessing group | 200 | 200  | 200     | 405  | 403 | 403   | 403    | 403   |
    | Group admin accessing group  | 200 | 200  | 200     | 405  | 200 | 200   | 204    | 403   |
    | Group PI accessing group     | 200 | 200  | 200     | 405  | 200 | 200   | 204    | 403   |
    | Staff user                   | 200 | 200  | 200     | 405  | 200 | 200   | 204    | 405   |
    """

    endpoint_pattern = '/users/researchgroups/{pk}/'
    fixtures = ['multi_research_group.yaml']

    def test_anonymous_user_permissions(self) -> None:
        """Test unauthenticated users cannot access resources."""

        endpoint = self.endpoint_pattern.format(pk=1)
        self.assert_http_responses(
            endpoint,
            get=status.HTTP_403_FORBIDDEN,
            head=status.HTTP_403_FORBIDDEN,
            options=status.HTTP_403_FORBIDDEN,
            post=status.HTTP_403_FORBIDDEN,
            put=status.HTTP_403_FORBIDDEN,
            patch=status.HTTP_403_FORBIDDEN,
            delete=status.HTTP_403_FORBIDDEN,
            trace=status.HTTP_403_FORBIDDEN
        )

    def test_authenticated_user_different_group(self) -> None:
        """Test authenticated users have read-only permissions to research groups."""

        # Define a user / record endpoint from DIFFERENT research groups
        endpoint = self.endpoint_pattern.format(pk=1)
        user = User.objects.get(username='member_2')
        self.client.force_authenticate(user=user)

        self.assert_http_responses(
            endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_405_METHOD_NOT_ALLOWED,
            put=status.HTTP_403_FORBIDDEN,
            patch=status.HTTP_403_FORBIDDEN,
            delete=status.HTTP_403_FORBIDDEN,
            trace=status.HTTP_403_FORBIDDEN,
        )

    def test_authenticated_group_member(self) -> None:
        """Test group members have read-only permissions for their own research group."""

        endpoint = self.endpoint_pattern.format(pk=1)
        user = User.objects.get(username='member_1')
        self.client.force_authenticate(user=user)

        self.assert_http_responses(
            endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_405_METHOD_NOT_ALLOWED,
            put=status.HTTP_403_FORBIDDEN,
            patch=status.HTTP_403_FORBIDDEN,
            delete=status.HTTP_403_FORBIDDEN,
            trace=status.HTTP_403_FORBIDDEN,
        )

    def test_authenticated_group_admin(self) -> None:
        """Test group admins have read and write permissions for their own research group."""

        endpoint = self.endpoint_pattern.format(pk=1)
        user = User.objects.get(username='group_admin_1')
        self.client.force_authenticate(user=user)

        self.assert_http_responses(
            endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_405_METHOD_NOT_ALLOWED,
            put=status.HTTP_200_OK,
            patch=status.HTTP_200_OK,
            delete=status.HTTP_204_NO_CONTENT,
            trace=status.HTTP_403_FORBIDDEN,
            put_body={'name': 'Research Group 3', 'pi': 1, 'admins': [2], 'members': [3]},
            patch_body={'admins': []},
        )

    def test_authenticated_group_pi(self) -> None:
        """Test group PIs have read and write permissions for their own research group."""

        endpoint = self.endpoint_pattern.format(pk=1)
        user = User.objects.get(username='pi_1')
        self.client.force_authenticate(user=user)

        self.assert_http_responses(
            endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_405_METHOD_NOT_ALLOWED,
            put=status.HTTP_200_OK,
            patch=status.HTTP_200_OK,
            delete=status.HTTP_204_NO_CONTENT,
            trace=status.HTTP_403_FORBIDDEN,
            put_body={'name': 'Research Group 3', 'pi': 1, 'admins': [2], 'members': [3]},
            patch_body={'admins': []},
        )

    def test_staff_user_permissions(self) -> None:
        """Test staff users have read and write permissions."""

        endpoint = self.endpoint_pattern.format(pk=1)
        user = User.objects.get(username='staff_user')
        self.client.force_authenticate(user=user)

        self.assert_http_responses(
            endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_405_METHOD_NOT_ALLOWED,
            put=status.HTTP_200_OK,
            patch=status.HTTP_200_OK,
            delete=status.HTTP_204_NO_CONTENT,
            trace=status.HTTP_405_METHOD_NOT_ALLOWED,
            put_body={'name': 'Research Group 3', 'pi': 1, 'admins': [2], 'members': [3]},
            patch_body={'admins': []},
        )
