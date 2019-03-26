from rest_framework import viewsets, generics
from .models import Announcement, Category, ImagePath
from .serializers import AnnouncementSerializer, CategorySerializer, ImageSerializer
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.db.models import F


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

    def get_serializer_class(self):
        if self.action == 'images':
            return ImageSerializer
        return self.serializer_class

    @action(detail=True, methods=['post', 'get'])
    def images(self, request, *args, **kwargs):
        if request.method == 'GET':
            queryset = ImagePath.objects.filter(announcement_id=kwargs['pk'])
            serializer = ImageSerializer(queryset, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            return Response(request.data)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



class CategoryViewset(viewsets.ViewSet):
    """
    retrieve:
        Returns a specific category with its children and parent

    list:
        Return a list of all categories with their children and parent

    leaves:
        Return a list of categories that haven't got any children
    """
    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def leaves(self, request, *args, **kwargs):
        #  A leaf node may be identified by 'right == left + 1'
        queryset = Category.objects.filter(lft=F('rght')-1)
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
