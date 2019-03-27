from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Announcement, Category, ImagePath
# from .models import AdvSiteUser
# from django.contrib.auth.admin import UserAdmin
# from .forms import AdvSiteUserChangeForm, AdvSiteUserCreationForm
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


# class AdvSiteUserAdmin(UserAdmin):
#     add_form = AdvSiteUserCreationForm
#     form = AdvSiteUserChangeForm
#     model = AdvSiteUser
#     list_display = ['email', 'username', 'firstname', "lastname"]
#
#
# admin.site.register(AdvSiteUser, AdvSiteUserAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Category, DraggableMPTTAdmin)
