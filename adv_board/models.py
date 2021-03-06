from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth import get_user_model
from adv_platform.settings import AUTH_USER_MODEL
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Announcement(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    content = models.TextField(max_length=5000)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    bargain = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    category = TreeForeignKey('Category', verbose_name='parent category',
                              related_name='announcements', on_delete=models.SET_NULL,
                              blank=True, null=True)
    author = models.ForeignKey(
      AUTH_USER_MODEL,
      on_delete=models.CASCADE
    )
    last_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ImagePath(models.Model):
    valid_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
    ]

    class Meta:
        unique_together = ("path", "announcement")

    path = models.URLField(max_length=150, blank=True)
    announcement = models.ForeignKey('Announcement', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.path
