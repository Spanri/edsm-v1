from django.contrib import admin
from .models import Doc

@admin.register(Doc)
class DocAdmin(admin.ModelAdmin):
    # fields = ('title', 'owner', 'date', 'common')
    pass
    
# admin.site.register(Doc, DocAdmin)
