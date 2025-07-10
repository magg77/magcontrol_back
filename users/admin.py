from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # tu modelo de usuario personalizado

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'groups')  # 👈 importante

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff', 'groups')}
        ),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')  # 👈 esto muestra bien los permisos y grupos
