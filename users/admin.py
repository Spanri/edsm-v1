from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserProfile, Notif

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

@admin.register(Notif)
class NotifAdmin(admin.ModelAdmin):
    list_display = ('user', 'doc', 'status', 'queue', 'id')
    search_fields = ('id',)
    ordering = ('id',)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, 
            {'fields': ('email', 'password', 'username',
            'is_get_notif_email')}
        ),
        (_('Permissions'),
            {'fields': 
                ('is_active', 
                'is_staff', 
                'is_superuser',
                'groups', 
                'user_permissions')
            }
        ),
        (_('Important dates'), 
            {'fields': ('last_login', 'date_joined')}
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_staff', 'is_superuser', 'id')
    search_fields = ('email',)
    ordering = ('email',)
    inlines = (UserProfileInline,)
