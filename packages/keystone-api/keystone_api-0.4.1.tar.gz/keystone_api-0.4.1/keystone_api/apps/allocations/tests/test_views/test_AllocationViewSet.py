"""Unit tests for the `AllocationViewSet` class."""

from django.test import RequestFactory, TestCase

from apps.allocations.models import Allocation
from apps.allocations.views import AllocationViewSet
from apps.users.models import ResearchGroup, User


class GetQueryset(TestCase):
    """Test the filtering of database records based on user permissions."""

    fixtures = ['common.yaml']

    def test_get_queryset_for_staff_user(self) -> None:
        """Test staff users can query all reviews."""

        request = RequestFactory()
        request.user = User.objects.get(username='staff')

        viewset = AllocationViewSet()
        viewset.request = request

        expected_queryset = Allocation.objects.all()
        self.assertQuerySetEqual(expected_queryset, viewset.get_queryset(), ordered=False)

    def test_get_queryset_for_non_staff_user(self) -> None:
        """Test non-staff users can only query allocations for their own research groups."""

        user = User.objects.get(username='user1')
        group = ResearchGroup.objects.get(name='group1')

        request = RequestFactory()
        request.user = user

        viewset = AllocationViewSet()
        viewset.request = request

        expected_queryset = Allocation.objects.filter(request__group__in=[group.id])
        self.assertQuerySetEqual(expected_queryset, viewset.get_queryset(), ordered=False)
