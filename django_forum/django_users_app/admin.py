from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User

# @admin.register(UserAdmin)
# class UserAdmin(UserAdmin):
#     list_display = ('active', 'username', 'email', 'first_name', 'last_name')
#     list_filter = ('active', 'username', 'email')
#     search_fields = ('username', 'email', 'first_name', 'last_name')
#     actions = ['activate_user']

#     def activate_image(self, request, queryset):
#         queryset.update(active=True)
