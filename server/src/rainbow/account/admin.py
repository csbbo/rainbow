from django.contrib import admin
from account.models import *


admin.site.site_header = 'ADMIN'
admin.site.site_title = 'admin'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'tel', 'last_login_time', 'create_time', 'update_time')
    list_display_links = ('id',)
    search_fields = list_display
