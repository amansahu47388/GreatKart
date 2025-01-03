from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    # Display these fields in the admin list view
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    
    # Make these fields clickable in the admin
    list_display_links = ('email', 'first_name', 'last_name')
    
    # These fields are read-only
    readonly_fields = ('last_login', 'date_joined')
    
    # Sort by date joined in descending order
    ordering = ('-date_joined',)

    # Required for custom user model
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    # Add search fields
    search_fields = ('email', 'first_name', 'last_name', 'username')
    
    # Add list filters
    list_filter = ('is_active', 'is_staff', 'is_superuser')

admin.site.register(Account, AccountAdmin)
