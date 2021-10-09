from django.contrib import admin

from apps.accounts.models import UserProfile
from django.contrib.auth.admin import UserAdmin

admin.site.register(UserProfile,UserAdmin)
