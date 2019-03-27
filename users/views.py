from rest_framework import viewsets, generics, mixins
from .models import AdvSiteUser
# from adv_board.models import Announcement
from .serializers import UserSerializer
from .serializers import AdvsTitleSerializer
from rest_framework import permissions
from adv_board.permissions import IsOwnerOrReadOnly
from .permissions import IsTheUserOrAdmin
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class UserListView(generics.ListAPIView):
    """
    Return a list of users
    """
    queryset = AdvSiteUser.objects.all()
    serializer_class = UserSerializer


class UserAddToFavsView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView):
    queryset = AdvSiteUser.objects.all()
    serializer_class = AdvsTitleSerializer
    permission_classes = (IsTheUserOrAdmin, permissions.IsAuthenticatedOrReadOnly,)

    """
    Return a list of announcements, favored by user
    """
    def get(self, request, *args, **kwargs):
        user = self.queryset.get(id=kwargs['user_id'])
        self.check_object_permissions(request, obj=user)
        queryset = user.favored_advs.all()
        print(queryset)
        serializer = AdvsTitleSerializer(queryset, many=True)
        print(serializer.data)
        # return Response(serializer.data)
        return self.list(request, *args, **kwargs)

    # """
    # Add an announcement to favored by its pk
    # """
    # def post(self, request, *args, **kwargs):
    #     user = self.queryset.get(id=kwargs['user_id'])
    #     self.check_object_permissions(request, obj=user)
    #     announcement = get_object_or_404(Announcement.objects.all(), title=request.data['title'])
    #     # user.favored_advs.add(announcement)
    #     # queryset = user.favored_advs.all()
    #     # serializer = AdvsTitleSerializer(queryset, many=True)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
