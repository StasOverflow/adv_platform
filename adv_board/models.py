from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.core.validators import ValidationError

from adv_platform.settings import ANNOUNCEMENT_IMAGE_LIMIT


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=5000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bargain = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    category = TreeForeignKey('Category', verbose_name='parent category',
                              related_name='announcements', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ImagePath(models.Model):
    valid_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
    ]

    path = models.URLField(max_length=150, blank=True)
    announcement = models.ForeignKey('Announcement', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.path

    def clean(self):
        if not any([self.path.endswith(e) for e in self.valid_extensions]):
            raise ValidationError(
                {'path': 'Unsupported image format'}
            )
        print(ImagePath.objects.filter(announcement=self.announcement).count())
        if ImagePath.objects.filter(announcement=self.announcement).count() > ANNOUNCEMENT_IMAGE_LIMIT:
            raise ValidationError(
                {'path': 'Maximum images limit reached: ({})'.format(ANNOUNCEMENT_IMAGE_LIMIT)}
            )
