from django.contrib import admin
from . import models as profile_models

# Register your models here.


@admin.register(profile_models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['display_name']
    list_filter = ['display_name']
    search_fields = ['display_name']
