from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name', 'username')
    filter_horizontal = ('groups', 'user_permissions')
    list_filter = ('is_active', 'is_staff', 'is_admin', 'is_superadmin', 'groups')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'username', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superadmin', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'username', 'phone', 'password1', 'password2'),
        }),
    )
admin.site.register(Account, AccountAdmin)