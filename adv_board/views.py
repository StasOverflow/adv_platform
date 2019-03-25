from rest_framework import viewsets, generics
from .models import Announcement
from .serializers import AnnouncementSerializer


class AnnouncementViewset(viewsets.ModelViewSet):
    """
    retrieve:
        Return a specific announcement

    list:
        Return a list of all announcements.

    create:
        Create a new announcement.

    destroy:
        Delete an announcement.

    update:
        Update an announcement.

    partial_update:
        Update an announcement.
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
