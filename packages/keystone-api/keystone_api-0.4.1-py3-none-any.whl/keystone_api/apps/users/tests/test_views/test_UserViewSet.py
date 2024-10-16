"""Unit tests for the `UserViewSet` class."""

from django.test import RequestFactory, TestCase

from apps.users.models import User
from apps.users.serializers import PrivilegeUserSerializer, RestrictedUserSerializer
from apps.users.views import UserViewSet


class GetSerializerClass(TestCase):
    """Test the `get_serializer_class` method."""

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.staff_user = User.objects.create(username='staffuser', is_staff=True)
        self.regular_user = User.objects.create(username='regularuser', is_staff=False)

    def test_get_serializer_class_for_staff_user(self) -> None:
        """Test the `PrivilegeUserSerializer` serializer is returned for a staff user."""

        request = self.factory.get('/users/')
        request.user = self.staff_user
        view = UserViewSet(request=request)

        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, PrivilegeUserSerializer)

    def test_get_serializer_class_for_regular_user(self) -> None:
        """Test the `RestrictedUserSerializer` serializer is returned for a generic user."""

        request = self.factory.get('/users/')
        request.user = self.regular_user
        view = UserViewSet(request=request)

        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, RestrictedUserSerializer)
