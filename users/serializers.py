from rest_framework import serializers
from .models import AdvSiteUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvSiteUser
        fields = ('username', 'firstname', 'lastname')
