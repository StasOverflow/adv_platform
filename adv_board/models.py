from django.db import models
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


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
                              related_name='adv', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
