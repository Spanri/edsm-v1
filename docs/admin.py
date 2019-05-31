from django.contrib import admin
from .models import Doc, FileCabinet

@admin.register(Doc)
class DocAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'common', 'id')
    search_fields = ('id',)
    ordering = ('id',)


@admin.register(FileCabinet)
class FileCabinetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id',)
    ordering = ('id',)
