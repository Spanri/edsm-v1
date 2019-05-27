from django.contrib import admin
from .models import Doc

@admin.register(Doc)
class DocAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'common', 'id')
    search_fields = ('id',)
    ordering = ('id',)
