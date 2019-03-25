from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Announcement
from .models import Category


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'bargain', "created_on", "category")


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Category, DraggableMPTTAdmin)
