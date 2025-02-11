"""
Admin configuration for users app
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserSettings

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin"""
    list_display = (
        'email', 'get_full_name', 'is_instructor', 
        'is_active', 'is_staff', 'date_joined'
    )
    list_filter = ('is_instructor', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'avatar', 'bio')
        }),
        (_('Instructor info'), {
            'fields': ('is_instructor', 'title', 'expertise', 'website'),
            'classes': ('collapse',),
            'description': _('Additional fields for instructor accounts')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    def get_full_name(self, obj):
        """Get user's full name"""
        return obj.get_full_name()
    get_full_name.short_description = _('Full Name')
    get_full_name.admin_order_field = 'first_name'

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    """User Settings admin"""
    list_display = (
        'user', 'course_updates', 'marketing_emails',
        'public_profile', 'show_progress', 'updated_at'
    )
    list_filter = ('course_updates', 'marketing_emails', 'public_profile', 'show_progress')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('User'), {
            'fields': ('user',)
        }),
        (_('Notification Settings'), {
            'fields': ('course_updates', 'marketing_emails')
        }),
        (_('Privacy Settings'), {
            'fields': ('public_profile', 'show_progress')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """Make user field readonly when editing"""
        if obj:
            return self.readonly_fields + ('user',)
        return self.readonly_fields