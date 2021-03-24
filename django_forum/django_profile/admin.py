from django.contrib import admin
from .models import Profile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['display_name']
    list_filter = ['display_name']
    search_fields = ['display_name']