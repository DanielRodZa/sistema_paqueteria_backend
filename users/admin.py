from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Añade el campo 'role' al listado y a los campos editables del admin
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role', 'sucursal')
    fieldsets = UserAdmin.fieldsets + (
        ('Roles y Sucursal', {'fields': ('role', 'sucursal')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'sucursal',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)