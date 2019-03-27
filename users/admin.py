from django.contrib import admin
from .models import AdvSiteUser
from .forms import AdvSiteUserCreationForm, AdvSiteUserChangeForm
from django.contrib.auth.admin import UserAdmin


class AdvSiteUserAdmin(UserAdmin):
    add_form = AdvSiteUserCreationForm
    form = AdvSiteUserChangeForm
    model = AdvSiteUser
    list_display = ['username', 'email', 'firstname', "lastname"]


admin.site.register(AdvSiteUser, AdvSiteUserAdmin)
