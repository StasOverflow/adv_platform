from django.contrib import admin
from .models import Announcement


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'bargain', )


admin.site.register(Announcement, AnnouncementAdmin)
