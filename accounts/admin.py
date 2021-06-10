from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _



class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['phone_no','email','first_name','last_name']
    fieldsets = (
        (None, {'fields': ('phone_no','password')}),
        (_('Personal Info'), {'fields': ('first_name','last_name','email')}),
        (_('Permissions'), {'fields': ('is_active','is_staff','is_superuser', 'is_manager', 'has_permission_to_view_prices', 'user_permissions', 'groups')}),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_no','password1','password2')
        }),
    )



admin.site.register(User,UserAdmin)