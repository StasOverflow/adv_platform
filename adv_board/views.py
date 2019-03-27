from rest_framework import viewsets, generics
from .models import Announcement, Category, ImagePath
from .serializers import AnnouncementSerializer, CategorySerializer, ImageSerializer
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.db.models import F
from rest_framework.serializers import ValidationError
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly


class AnnouncementListView(generics.ListAPIView):
    """
    Returns a list of all despite its status, available only for adminuser
    """

    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = (permissions.IsAdminUser,)


class AnnouncementViewset(viewsets.ModelViewSet):
    """
    retrieve:
        Return a specific announcement

    list:
        Return a list of ACTIVE announcements.
        possible arguments:

            category: Any of category names on site

            price_limit: any price limit
                expected output: announcements with a price less or equals to given

    create:
        Create a new announcement.

    destroy:
        Delete an announcement.

    update:
        Update an announcement.

    partial_update:
        Update an announcement.
    """
    # queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def get_queryset(self):
        """
        Optionally restricts the returned query to a given category and its
        subcategories by filtering against a `category` query parameter in the URL.
        """
        queryset = Announcement.objects.filter(is_active=True)

        category = self.request.query_params.get('category', None)
        if category is not None:
            category = Category.objects.get(name=category)
            queryset = queryset.filter(category__in=category.get_descendants(include_self=True))

        """
        Optionally restricts the returned query to a given price limit
        """
        price_limit = self.request.query_params.get('price_limit', None)

        if price_limit is not None:
            try:
                price_limit = float(price_limit)
                queryset = queryset.filter(price__lte=price_limit)
            except Exception as e:
                pass

        return queryset

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)

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
        if self.queryset.get(id=kwargs['pk']):
            if request.method == 'GET':
                queryset = self.queryset.filter(announcement_id=kwargs['pk'])
                serializer = ImageSerializer(queryset, many=True)
                return Response(serializer.data)

            elif request.method == 'POST':
                """
                Only a ceratain amout of images can be applied to an announcement
                """
                serializer = AnnouncementSerializer
                try:
                    data = serializer.multiple_image_instances_prepare(request.data, pk=kwargs['pk'])
                    for instance in data:
                        instance.save()
                except ValidationError as e:
                    return Response("{'error_message': '{}'".format(e),
                                    status=status.HTTP_400_BAD_REQUEST)
                return Response(data, status=status.HTTP_200_OK)
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

    queryset = Category.objects.all()

    def list(self, request):
        queryset = self.queryset
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.queryset
        category = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def leaves(self, request, *args, **kwargs):
        #  A leaf node may be identified by 'right == left + 1'
        queryset = Category.objects.filter(lft=F('rght')-1)
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
