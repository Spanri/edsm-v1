from django.contrib import admin
from .models import Doc, FileCabinet, Block, Reg

@admin.register(Doc)
class DocAdmin(admin.ModelAdmin):
    list_display = ('id', 'reg', 'title', 'date', 'common', 'cancel_description')
    search_fields = ('id',)
    ordering = ('id',)

@admin.register(Reg)
class RegAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id',)
    ordering = ('id',)

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'data', 'hash', 'previous_hash')
    search_fields = ('id',)
    ordering = ('id',)

@admin.register(FileCabinet)
class FileCabinetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id',)
    ordering = ('id',)
