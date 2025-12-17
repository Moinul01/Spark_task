from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'source', 'is_active', 'uploaded_at')
    list_filter = ('document_type', 'is_active', 'uploaded_at')
    search_fields = ('title', 'content', 'source')
    readonly_fields = ('uploaded_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'content', 'document_type', 'source', 'is_active')
        }),
        ('Dates', {
            'fields': ('uploaded_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )