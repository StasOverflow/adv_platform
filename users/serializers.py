from rest_framework import serializers
from .models import AdvSiteUser
from adv_board.serializers import AnnouncementSerializer, Announcement


class AdvsTitleSerializer(serializers.ModelSerializer):

    favored_advs = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Announcement.objects.all(),
        many=True
     )

    class Meta:
        model = AdvSiteUser
        fields = ('favored_advs', )


class UserSerializer(serializers.ModelSerializer):

    favored_advs = AdvsTitleSerializer(read_only=True, many=True)

    class Meta:
        model = AdvSiteUser
        fields = ('username', 'firstname', 'lastname', 'favored_advs')

