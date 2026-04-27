from django.contrib import admin
from .models import Asset, Tag, ChangeLog


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display  = ['title', 'asset_type', 'status', 'created_at']
    list_filter   = ['asset_type', 'status']
    search_fields = ['title', 'description']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    list_display  = ['asset', 'change_summary', 'changed_at']
    readonly_fields = ['asset', 'change_summary', 'snapshot', 'changed_at']