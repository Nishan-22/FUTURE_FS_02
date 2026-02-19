from django.contrib import admin
from .models import Lead, Note

class NoteInline(admin.TabularInline):
    model = Note
    extra = 1

class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'source', 'status', 'created_at')
    list_filter = ('status', 'source')
    search_fields = ('name', 'email')
    inlines = [NoteInline]

admin.site.register(Lead, LeadAdmin)
