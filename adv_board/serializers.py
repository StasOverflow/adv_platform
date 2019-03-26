from rest_framework import serializers
from .models import Announcement, Category, ImagePath
from adv_platform.settings import ANNOUNCEMENT_IMAGE_LIMIT
# from django.core.validators import ValidationError
from rest_framework.serializers import ValidationError


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImagePath
        fields = ('path', )


class AnnouncementSerializer(serializers.ModelSerializer):

    images = ImageSerializer(many=True)
    # images = serializers.HyperlinkedRelatedField(many=True, view_name='adv-images', read_only=True)

    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),
     )

    class Meta:
        model = Announcement
        fields = ('id', 'title', 'content', 'price', 'bargain', 'created_on', 'category', 'images',)

    @classmethod
    def images_per_instance_validator(cls, pk, path_list, image_paths):

        # check if new list of urls contains any and not exceeding the limit
        if len(path_list) > ANNOUNCEMENT_IMAGE_LIMIT:
            raise ValidationError("Cannot insert {} images, max {}".format(
                len(path_list), ANNOUNCEMENT_IMAGE_LIMIT
            ))
        # check if url ends with image extension
        image_list = list()
        for path in path_list:
            if not any([path.endswith(e) for e in ImagePath.valid_extensions]):
                raise ValidationError("Incorrect image format, use one of {}".format(
                    ImagePath.valid_extensions,
                ))
            if path not in image_paths:
                image_list.append(ImagePath(announcement_id=pk, path=path))
            else:
                # Duplicate images won't be inserted again
                pass
        return image_list

    @classmethod
    def multiple_image_instances_prepare(cls, images, pk):
        path_list = [arg['path'] for arg in images if 'path' in arg]
        images = ImagePath.objects.filter(announcement_id=pk)
        image_paths = images.values_list('path', flat=True).order_by('id')
        images = cls.images_per_instance_validator(pk=pk, path_list=path_list, image_paths=image_paths)
        return images

    def create(self, validated_data):

        images = validated_data.pop('images')
        obj = Announcement.objects.create(**validated_data)
        images = self.multiple_image_instances_prepare(images, obj.id)
        for image in images:
            image.save()
        return obj


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
