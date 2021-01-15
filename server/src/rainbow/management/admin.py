from django.contrib import admin
from management.models import Config


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'create_time', 'update_time')
