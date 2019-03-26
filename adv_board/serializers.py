from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import Announcement, Category, ImagePath


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImagePath
        fields = ('path', )


class AnnouncementSerializer(serializers.ModelSerializer):

    images = ImageSerializer(many=True)

    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),
     )

    class Meta:
        model = Announcement
        fields = ('id', 'title', 'content', 'price', 'bargain', 'created_on', 'category', 'images')


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
        fields = ('id', 'name', 'parent', 'children',)
