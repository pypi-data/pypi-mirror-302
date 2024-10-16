"""Application logic for rendering HTML templates and handling HTTP requests.

View objects handle the processing of incoming HTTP requests and return the
appropriately rendered HTML template or other HTTP response.
"""

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .models import *
from .permissions import *
from .serializers import *
from ..users.models import ResearchGroup

__all__ = [
    'AllocationViewSet',
    'AllocationRequestViewSet',
    'AllocationRequestReviewViewSet',
    'ClusterViewSet',
]


class AllocationViewSet(viewsets.ModelViewSet):
    """Manage allocations for user research groups."""

    queryset = Allocation.objects.all()
    serializer_class = AllocationSerializer
    permission_classes = [permissions.IsAuthenticated, StaffWriteGroupRead]

    def get_queryset(self) -> list[Allocation]:
        """Return a list of allocations for the currently authenticated user."""

        if self.request.user.is_staff:
            return self.queryset

        research_groups = ResearchGroup.objects.groups_for_user(self.request.user)
        return Allocation.objects.filter(request__group__in=research_groups)


class AllocationRequestViewSet(viewsets.ModelViewSet):
    """Manage allocation requests submitted by user research groups."""

    queryset = AllocationRequest.objects.all()
    serializer_class = AllocationRequestSerializer
    permission_classes = [permissions.IsAuthenticated, GroupAdminCreateGroupRead]

    def get_queryset(self) -> list[AllocationRequest]:
        """Return a list of allocation requests for the currently authenticated user."""

        if self.request.user.is_staff:
            return self.queryset

        research_groups = ResearchGroup.objects.groups_for_user(self.request.user)
        return AllocationRequest.objects.filter(group__in=research_groups)


class AllocationRequestReviewViewSet(viewsets.ModelViewSet):
    """Manage reviews of allocation request submitted by administrators."""

    queryset = AllocationRequestReview.objects.all()
    serializer_class = AllocationRequestReviewSerializer
    permission_classes = [permissions.IsAuthenticated, StaffWriteGroupRead]

    def get_queryset(self) -> list[Allocation]:
        """Return a list of allocation reviews for the currently authenticated user."""

        if self.request.user.is_staff:
            return self.queryset

        research_groups = ResearchGroup.objects.groups_for_user(self.request.user)
        return AllocationRequestReview.objects.filter(request__group__in=research_groups)

    def create(self, request, *args, **kwargs) -> Response:
        """Create a new `AllocationRequestReview` object."""

        data = request.data.copy()
        data.setdefault('reviewer', request.user.pk)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ClusterViewSet(viewsets.ModelViewSet):
    """Configuration settings for managed Slurm clusters."""

    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
    permission_classes = [permissions.IsAuthenticated, StaffWriteAuthenticatedRead]
