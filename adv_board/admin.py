from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Announcement, Category, ImagePath
from adv_platform import settings


class ImagePathAdmin(admin.TabularInline):
    model = ImagePath
    extra = 1
    max_num = settings.ANNOUNCEMENT_IMAGE_LIMIT


class AnnouncementAdmin(admin.ModelAdmin):
    inlines = [
        ImagePathAdmin,
    ]

    list_display = ('title', 'content', 'price', 'bargain', "created_on", "category",)


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Category, DraggableMPTTAdmin)
