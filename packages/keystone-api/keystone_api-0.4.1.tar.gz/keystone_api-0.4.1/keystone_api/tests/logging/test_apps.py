"""Function tests for the `/logs/apps/` endpoint."""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User
from tests.utils import CustomAsserts


class EndpointPermissions(APITestCase, CustomAsserts):
    """Test endpoint user permissions.

    Endpoint permissions are tested against the following matrix of HTTP responses.

    | Authentication      | GET | HEAD | OPTIONS | POST | PUT | PATCH | DELETE | TRACE |
    |---------------------|-----|------|---------|------|-----|-------|--------|-------|
    | Anonymous User      | 403 | 403  | 403     | 403  | 403 | 403   | 403    | 403   |
    | Authenticated User  | 403 | 403  | 403     | 403  | 403 | 403   | 403    | 403   |
    | Staff User          | 200 | 200  | 200     | 405  | 405 | 405   | 405    | 405   |
    """

    endpoint = '/logs/apps/'
    fixtures = ['multi_research_group.yaml']

    def test_anonymous_user_permissions(self) -> None:
        """Test unauthenticated users cannot access resources."""

        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_403_FORBIDDEN,
            head=status.HTTP_403_FORBIDDEN,
            options=status.HTTP_403_FORBIDDEN,
            post=status.HTTP_403_FORBIDDEN,
            put=status.HTTP_403_FORBIDDEN,
            patch=status.HTTP_403_FORBIDDEN,
            delete=status.HTTP_403_FORBIDDEN,
            trace=status.HTTP_403_FORBIDDEN
        )

    def test_authenticated_user_permissions(self) -> None:
        """Test general authenticated users are returned a 403 status code for all request types."""

        user = User.objects.get(username='generic_user')
        self.client.force_authenticate(user=user)

        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_403_FORBIDDEN,
            head=status.HTTP_403_FORBIDDEN,
            options=status.HTTP_403_FORBIDDEN,
            post=status.HTTP_403_FORBIDDEN,
            put=status.HTTP_403_FORBIDDEN,
            patch=status.HTTP_403_FORBIDDEN,
            delete=status.HTTP_403_FORBIDDEN,
            trace=status.HTTP_403_FORBIDDEN
        )

    def test_staff_user_permissions(self) -> None:
        """Test staff users have read-only permissions."""

        user = User.objects.get(username='staff_user')
        self.client.force_authenticate(user=user)

        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_405_METHOD_NOT_ALLOWED,
            put=status.HTTP_405_METHOD_NOT_ALLOWED,
            patch=status.HTTP_405_METHOD_NOT_ALLOWED,
            delete=status.HTTP_405_METHOD_NOT_ALLOWED,
            trace=status.HTTP_405_METHOD_NOT_ALLOWED
        )
