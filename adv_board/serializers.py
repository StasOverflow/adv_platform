from rest_framework import serializers
from .models import Announcement, Category, ImagePath
from adv_platform.settings import ANNOUNCEMENT_IMAGE_LIMIT
from rest_framework.serializers import ValidationError
from users.models import AdvSiteUser


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

    author_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    # # Get the current user from request context
    # def validate_author_id(self, value):
    #     return self.context['request'].user

    class Meta:
        model = Announcement
        fields = ('id', 'title', 'content', 'price', 'bargain', 'created_on', 'category', 'images', 'author_id')

    @classmethod
    def images_per_instance_validator(cls, pk, path_list, image_paths, for_update=False):

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
            if not for_update:
                if path not in image_paths:
                    image_list.append(ImagePath(announcement_id=pk, path=path))
                else:
                    # Duplicate images won't be inserted again
                    pass
            else:
                image_list.append(ImagePath(announcement_id=pk, path=path))
        return image_list

    @classmethod
    def multiple_image_instances_prepare(cls, images, pk, for_update=False):
        path_list = [arg['path'] for arg in images if 'path' in arg]
        images = ImagePath.objects.filter(announcement_id=pk)
        image_paths = images.values_list('path', flat=True).order_by('id')
        images = cls.images_per_instance_validator(pk=pk, path_list=path_list,
                                                   image_paths=image_paths, for_update=for_update)
        return images

    def create(self, validated_data):

        print(validated_data)

        images = validated_data.pop('images')
        obj = Announcement.objects.create(**validated_data)
        images = self.multiple_image_instances_prepare(images, obj.id)
        for image in images:
            image.save()
        return obj

    def update(self, instance, validated_data):
        images = None
        if 'images' in validated_data:
            images = validated_data.pop('images')
        obj = super().update(instance, validated_data)

        # basically removes all images and replace with new ones, if new list exists and valid
        try:
            validated_images = self.multiple_image_instances_prepare(images, obj.id, for_update=True)
            ImagePath.objects.filter(announcement_id=obj.id).delete()
            for image in validated_images:
                image.save()
        except ValidationError as e:
            raise e

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
