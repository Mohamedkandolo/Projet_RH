from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer

admin.register(Customer)
class UtilisateurAdmin(UserAdmin):
    """Administration des utilisateurs personnalisés"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_creation']
    list_filter = ['role', 'is_active', 'date_creation']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']
    readonly_fields = ['date_creation']


admin.site.register(Customer)