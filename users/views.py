from rest_framework import viewsets, generics
from .models import AdvSiteUser
from .serializers import UserSerializer


class UserListView(generics.ListAPIView):
    """
    Return a list of users
    """
    queryset = AdvSiteUser.objects.all()
    serializer_class = UserSerializer
