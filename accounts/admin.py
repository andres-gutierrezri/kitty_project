"""
Configuración del panel de administración de Django
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserRole, LoginHistory, ActiveSession


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """
    Administración de roles de usuario
    """
    list_display = ['name', 'description', 'created_at', 'updated_at']
    list_filter = ['name', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información del Rol', {
            'fields': ('name', 'description', 'permissions')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Administración personalizada de usuarios
    """
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    readonly_fields = ['date_joined', 'last_login', 'created_at', 'updated_at', 'last_login_ip']
    
    fieldsets = (
        ('Información de Autenticación', {
            'fields': ('username', 'password')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'birth_date', 'avatar', 'bio')
        }),
        ('Dirección', {
            'fields': ('address', 'city', 'country', 'postal_code'),
            'classes': ('collapse',)
        }),
        ('Permisos y Rol', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Información de Sesión', {
            'fields': ('email_verified', 'last_login', 'last_login_ip'),
            'classes': ('collapse',)
        }),
        ('Fechas Importantes', {
            'fields': ('date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Información de Autenticación', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Información Personal', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'phone_number'),
        }),
        ('Permisos y Rol', {
            'classes': ('wide',),
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    """
    Administración del historial de inicios de sesión
    """
    list_display = ['user', 'ip_address', 'login_time', 'logout_time', 'success']
    list_filter = ['success', 'login_time']
    search_fields = ['user__username', 'user__email', 'ip_address']
    readonly_fields = ['user', 'ip_address', 'user_agent', 'login_time', 'logout_time', 'success']
    # date_hierarchy = 'login_time'  # Comentado temporalmente por problemas de zona horaria con MySQL
    
    fieldsets = (
        ('Información de Usuario', {
            'fields': ('user',)
        }),
        ('Información de Conexión', {
            'fields': ('ip_address', 'user_agent', 'success')
        }),
        ('Tiempos', {
            'fields': ('login_time', 'logout_time')
        }),
    )
    
    def has_add_permission(self, request):
        """Desactivar la adición manual de registros"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Desactivar la edición de registros"""
        return False


@admin.register(ActiveSession)
class ActiveSessionAdmin(admin.ModelAdmin):
    """
    Administración de sesiones activas
    """
    list_display = ['user', 'device_info', 'browser_info', 'ip_address', 'last_activity', 'is_current']
    list_filter = ['is_current', 'created_at', 'last_activity']
    search_fields = ['user__username', 'user__email', 'ip_address', 'device_info']
    readonly_fields = ['user', 'session_key', 'ip_address', 'user_agent', 'device_info', 'browser_info', 'created_at', 'last_activity']
    
    fieldsets = (
        ('Información de Usuario', {
            'fields': ('user', 'is_current')
        }),
        ('Información de Sesión', {
            'fields': ('session_key', 'created_at', 'last_activity')
        }),
        ('Información del Dispositivo', {
            'fields': ('ip_address', 'device_info', 'browser_info', 'user_agent', 'location')
        }),
    )
    
    def has_add_permission(self, request):
        """Desactivar la adición manual de registros"""
        return False
