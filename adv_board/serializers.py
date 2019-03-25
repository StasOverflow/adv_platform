from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import Announcement
from .models import Category


class AnnouncementSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),
     )

    class Meta:
        model = Announcement
        fields = ('id', 'title', 'content', 'price', 'bargain', 'created_on', 'category')


class CategorySerializer(serializers.ModelSerializer):

    children = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Category.objects.all()
    )

    parent = serializers.SlugRelatedField(
        many=False,
        slug_field='name',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'children',)  # add here rest of the fields from model

