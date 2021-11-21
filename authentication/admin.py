from django.contrib import admin
from authentication.models import User


class UserAdmin(admin.ModelAdmin):

    list_display = ['id', 'username', 'email']
    search_fields = ['nome', 'email']
    list_filter = ['created_at']


admin.site.register(User, UserAdmin)

