from django.contrib import admin
from .models import Announcement


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'bargain', "created_on")


admin.site.register(Announcement, AnnouncementAdmin)
