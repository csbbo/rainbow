from django.contrib import admin
from photo.models import *


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'category', 'watch_num', 'thumb_num', 'download_num', 'create_time',
                    'update_time')
    list_display_links = ('id', 'name')
    search_fields = list_display
    list_filter = ('create_time',)
