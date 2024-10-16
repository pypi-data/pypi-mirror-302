"""Unit tests for the `AllocationRequestViewSet` class."""

from django.test import RequestFactory, TestCase

from apps.allocations.models import AllocationRequest
from apps.allocations.views import AllocationRequestViewSet
from apps.users.models import ResearchGroup, User


class GetQueryset(TestCase):
    """Test the filtering of database records based on user permissions."""

    fixtures = ['common.yaml']

    def test_get_queryset_for_staff_user(self) -> None:
        """Test staff users can query all reviews."""

        request = RequestFactory()
        request.user = User.objects.get(username='staff')

        viewset = AllocationRequestViewSet()
        viewset.request = request

        expected_queryset = AllocationRequest.objects.all()
        self.assertQuerySetEqual(expected_queryset, viewset.get_queryset(), ordered=False)

    def test_get_queryset_for_non_staff_user(self) -> None:
        """Test non-staff users can only query requests from their own research groups."""

        user = User.objects.get(username='user1')
        group = ResearchGroup.objects.get(name='group1')

        request = RequestFactory()
        request.user = user

        viewset = AllocationRequestViewSet()
        viewset.request = request

        expected_queryset = AllocationRequest.objects.filter(group__in=[group.id])
        self.assertQuerySetEqual(expected_queryset, viewset.get_queryset(), ordered=False)
