from rest_framework import viewsets, generics
from .models import Announcement, Category, ImagePath
from .serializers import AnnouncementSerializer, CategorySerializer, ImageSerializer
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.db.models import F
from adv_platform.settings import ANNOUNCEMENT_IMAGE_LIMIT
from django.core.validators import ValidationError


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

    @action(detail=True, methods=['post', 'get', 'delete'])
    def images(self, request, *args, **kwargs):
        """
        get:
            Get a list of images for a certain announcement

        post:
            Insert a list of images for a certain announcement

        delete:
            Delete a whole list of images for a certain announcement
        """
        if Announcement.objects.get(id=kwargs['pk']):
            if request.method == 'GET':
                queryset = ImagePath.objects.filter(announcement_id=kwargs['pk'])
                serializer = ImageSerializer(queryset, many=True)
                return Response(serializer.data)

            elif request.method == 'POST':
                """
                Only a ceratain amout of images can be applied to an announcement
                """
                path_list = [arg['path'] for arg in request.data if 'path' in arg]
                images = ImagePath.objects.filter(announcement_id=kwargs['pk'])
                image_paths = images.values_list('path', flat=True).order_by('id')
                # check if new list of urls contains any and not exceeding the limit
                if len(path_list) > ANNOUNCEMENT_IMAGE_LIMIT:
                    return Response("{ 'error_message': 'Inserting {} images not allowed, "
                                    "max {}'".format(len(path_list), ANNOUNCEMENT_IMAGE_LIMIT),
                                    status=status.HTTP_400_BAD_REQUEST)
                elif not len(path_list):
                    return Response("{ 'error_message': 'empty request'".format(
                                    len(path_list), ANNOUNCEMENT_IMAGE_LIMIT),
                                    status=status.HTTP_400_BAD_REQUEST)
                # check if url ends with image extension
                for path in path_list:
                    if not any([path.endswith(e) for e in ImagePath.valid_extensions]):
                        return Response("{'error_message': 'Unsupported image format'",
                                        status=status.HTTP_400_BAD_REQUEST)
                    image_list = list()
                    if path not in image_paths:
                        image_list.append(ImagePath.objects.create(announcement_id=kwargs['pk'], path=path))
                    else:
                        # Duplicate images won't be inserted again
                        pass
                queryset = ImagePath.objects.filter(announcement_id=kwargs['pk'])
                serializer = ImageSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            elif request.method == 'DELETE':
                # Delete an entire collection of images per announcement
                ImagePath.objects.filter(announcement_id=kwargs['pk']).delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


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
