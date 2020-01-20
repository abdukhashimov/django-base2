from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User, Service
from django.utils.translation import gettext as _

class UserAdmin(BaseUserAdmin):
    """Custom user Admin"""
    ordering = ['id']
    list_display = ['id', 'email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # (_('Personal Info'),{'fields': ('id', )}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser',)
            }
        ),
        (_('Important Dates'), {
            'fields':('last_login', )
        }),
    )
    add_fieldsets = (
        (None, {'classes': ('wide'),
                'fields' : ('email',
                            'password1',
                            'password2')
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Service)