"""
Modelos para la gestión de usuarios y roles
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class UserRole(models.Model):
    """
    Modelo para definir los roles de usuario en el sistema
    """
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('USER', 'Usuario'),
        ('MODERATOR', 'Moderador'),
        ('GUEST', 'Invitado'),
    ]
    
    name = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        unique=True,
        verbose_name='Nombre del Rol'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )
    permissions = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Permisos Específicos'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Actualización'
    )
    
    class Meta:
        verbose_name = 'Rol de Usuario'
        verbose_name_plural = 'Roles de Usuario'
        ordering = ['name']
        db_table = 'user_roles'
    
    def __str__(self):
        return self.get_name_display()


class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser
    """
    # Validador para número de teléfono
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe estar en formato: '+999999999'. Hasta 15 dígitos permitidos."
    )
    
    # Campos adicionales
    role = models.ForeignKey(
        UserRole,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name='Rol'
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        verbose_name='Número de Teléfono'
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Nacimiento'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='Avatar'
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Biografía'
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Dirección'
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Ciudad'
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='País'
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Código Postal'
    )
    
    # Campos de auditoría
    email_verified = models.BooleanField(
        default=False,
        verbose_name='Email Verificado'
    )
    last_login_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='Última IP de Inicio de Sesión'
    )
    
    # Campos para eliminación de cuenta
    is_pending_deletion = models.BooleanField(
        default=False,
        verbose_name='Pendiente de Eliminación'
    )
    deletion_requested_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Solicitud de Eliminación'
    )
    scheduled_deletion_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha Programada de Eliminación'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Actualización'
    )
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-date_joined']
        db_table = 'custom_users'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def get_role_display(self):
        """Retorna el nombre del rol del usuario"""
        return self.role.get_name_display() if self.role else 'Sin Rol'
    
    def is_admin(self):
        """Verifica si el usuario es administrador"""
        return self.role and self.role.name == 'ADMIN'
    
    def is_moderator(self):
        """Verifica si el usuario es moderador"""
        return self.role and self.role.name == 'MODERATOR'
    
    def get_full_name_or_username(self):
        """Retorna el nombre completo o el username si no tiene nombre"""
        full_name = self.get_full_name()
        return full_name if full_name else self.username


class LoginHistory(models.Model):
    """
    Modelo para registrar el historial de inicios de sesión
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='login_history',
        verbose_name='Usuario'
    )
    ip_address = models.GenericIPAddressField(
        verbose_name='Dirección IP'
    )
    user_agent = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Navegador'
    )
    login_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Hora de Inicio de Sesión'
    )
    logout_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Hora de Cierre de Sesión'
    )
    success = models.BooleanField(
        default=True,
        verbose_name='Inicio Exitoso'
    )
    
    class Meta:
        verbose_name = 'Historial de Inicio de Sesión'
        verbose_name_plural = 'Historial de Inicios de Sesión'
        ordering = ['-login_time']
        db_table = 'login_history'
    
    def __str__(self):
        status = "Exitoso" if self.success else "Fallido"
        return f"{self.user.username} - {self.login_time.strftime('%Y-%m-%d %H:%M:%S')} - {status}"


class ActiveSession(models.Model):
    """
    Modelo para rastrear sesiones activas de usuarios
    Permite detectar múltiples inicios de sesión y gestionar sesiones remotamente
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='active_sessions',
        verbose_name='Usuario'
    )
    session_key = models.CharField(
        max_length=40,
        unique=True,
        verbose_name='Clave de Sesión'
    )
    ip_address = models.GenericIPAddressField(
        verbose_name='Dirección IP'
    )
    user_agent = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Agente de Usuario'
    )
    device_info = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Información del Dispositivo'
    )
    browser_info = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Información del Navegador'
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Ubicación'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Inicio'
    )
    last_activity = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actividad'
    )
    is_current = models.BooleanField(
        default=False,
        verbose_name='Sesión Actual'
    )
    
    class Meta:
        verbose_name = 'Sesión Activa'
        verbose_name_plural = 'Sesiones Activas'
        ordering = ['-last_activity']
        db_table = 'active_sessions'
        indexes = [
            models.Index(fields=['user', 'session_key']),
            models.Index(fields=['session_key']),
        ]
    
    def __str__(self):
        current = " (Actual)" if self.is_current else ""
        return f"{self.user.username} - {self.device_info or 'Dispositivo Desconocido'}{current}"
    
    def get_device_icon(self):
        """Retorna el ícono apropiado según el dispositivo"""
        user_agent_lower = self.user_agent.lower()
        
        if 'mobile' in user_agent_lower or 'android' in user_agent_lower or 'iphone' in user_agent_lower:
            return 'fa-mobile-alt'
        elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
            return 'fa-tablet-alt'
        else:
            return 'fa-desktop'
    
    def get_browser_name(self):
        """Extrae el nombre del navegador del user agent"""
        user_agent_lower = self.user_agent.lower()
        
        if 'edge' in user_agent_lower or 'edg/' in user_agent_lower:
            return 'Edge'
        elif 'chrome' in user_agent_lower and 'edg' not in user_agent_lower:
            return 'Chrome'
        elif 'firefox' in user_agent_lower:
            return 'Firefox'
        elif 'safari' in user_agent_lower and 'chrome' not in user_agent_lower:
            return 'Safari'
        elif 'opera' in user_agent_lower or 'opr/' in user_agent_lower:
            return 'Opera'
        else:
            return 'Desconocido'
    
    def get_os_name(self):
        """Extrae el nombre del sistema operativo del user agent"""
        user_agent_lower = self.user_agent.lower()
        
        if 'windows' in user_agent_lower:
            return 'Windows'
        elif 'mac os' in user_agent_lower or 'macos' in user_agent_lower:
            return 'macOS'
        elif 'linux' in user_agent_lower:
            return 'Linux'
        elif 'android' in user_agent_lower:
            return 'Android'
        elif 'iphone' in user_agent_lower or 'ipad' in user_agent_lower:
            return 'iOS'
        else:
            return 'Desconocido'
