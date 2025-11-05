"""
Vistas para la gestión de autenticación y usuarios
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from datetime import timedelta
import json
import re
from .models import CustomUser, UserRole, LoginHistory
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, ChangePasswordForm


def get_client_ip(request):
    """Obtiene la dirección IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def html_to_plain_text(html_content):
    """
    Convierte contenido HTML a texto plano para emails
    Elimina tags HTML y formatea el texto de manera legible
    """
    # Eliminar scripts y estilos
    text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    
    # Reemplazar <br> y <p> con saltos de línea
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'</p>', '\n\n', text)
    text = re.sub(r'<p[^>]*>', '', text)
    
    # Reemplazar <li> con bullets
    text = re.sub(r'<li[^>]*>', '  • ', text)
    text = re.sub(r'</li>', '\n', text)
    
    # Eliminar todos los tags HTML restantes
    text = strip_tags(text)
    
    # Limpiar espacios múltiples
    text = re.sub(r' +', ' ', text)
    
    # Limpiar líneas vacías múltiples
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    
    # Limpiar espacios al inicio/final de cada línea
    text = '\n'.join(line.strip() for line in text.split('\n'))
    
    return text.strip()


def send_html_email(subject, plain_message, html_message, from_email, recipient_list, fail_silently=False):
    """
    Envía un email con versión HTML y texto plano.
    En desarrollo (consola): solo muestra texto plano
    En producción (SMTP): envía ambas versiones (multipart)
    """
    from kitty_glow.local_settings import IS_DEPLOYED
    
    if IS_DEPLOYED:
        # Producción: Enviar email multipart (HTML + texto plano)
        msg = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=from_email,
            to=recipient_list
        )
        msg.attach_alternative(html_message, "text/html")
        msg.send(fail_silently=fail_silently)
    else:
        # Desarrollo: Solo enviar texto plano a la consola
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=fail_silently
        )


@csrf_protect
def login_view(request):
    """
    Vista para el inicio de sesión de usuarios
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            # Determinar si es email o username
            username = username_or_email
            if '@' in username_or_email:
                # Es un email, buscar el usuario por email
                try:
                    user_obj = CustomUser.objects.get(email=username_or_email)
                    username = user_obj.username
                except CustomUser.DoesNotExist:
                    username = username_or_email  # Mantener el valor para que falle la autenticación
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Verificar si la cuenta está pendiente de eliminación
                if user.is_pending_deletion:
                    # Cancelar la eliminación programada
                    user.is_pending_deletion = False
                    user.deletion_requested_at = None
                    user.scheduled_deletion_date = None
                    user.is_active = True
                    user.save()
                    
                    messages.success(
                        request,
                        '¡Bienvenido de nuevo! La eliminación de tu cuenta ha sido cancelada automáticamente.'
                    )
                
                # Verificar si la cuenta está activada
                if not user.is_active:
                    messages.error(
                        request, 
                        'Tu cuenta no ha sido verificada. Por favor, revisa tu correo electrónico '
                        'para activar tu cuenta. Si no recibiste el email, contacta con soporte.'
                    )
                    return render(request, 'accounts/login.html', {'form': form, 'page_title': 'Iniciar Sesión'})
                
                login(request, user)
                
                # Configurar duración de la sesión
                if not remember_me:
                    request.session.set_expiry(0)  # Cerrar sesión al cerrar navegador
                else:
                    request.session.set_expiry(1209600)  # 2 semanas
                
                # Registrar inicio de sesión
                user.last_login_ip = get_client_ip(request)
                user.save(update_fields=['last_login_ip'])
                
                # Crear registro de historial
                LoginHistory.objects.create(
                    user=user,
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
                    success=True
                )
                
                # Enviar notificación de inicio de sesión por email
                try:
                    send_login_notification(request, user)
                except Exception as e:
                    # Log el error pero no interrumpir el login
                    print(f"Error al enviar notificación de login: {e}")
                
                messages.success(request, f'¡Bienvenido de nuevo, {user.get_full_name_or_username()}!')
                
                # Redirigir según el rol
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                elif user.is_admin():
                    return redirect('accounts:admin_dashboard')
                else:
                    return redirect('accounts:dashboard')
            else:
                # Registrar intento fallido
                try:
                    failed_user = CustomUser.objects.get(username=username)
                    LoginHistory.objects.create(
                        user=failed_user,
                        ip_address=get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
                        success=False
                    )
                except CustomUser.DoesNotExist:
                    pass
                
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = UserLoginForm()
    
    context = {
        'form': form,
        'page_title': 'Iniciar Sesión',
    }
    return render(request, 'accounts/login.html', context)


@csrf_protect
def register_view(request):
    """
    Vista para el registro de nuevos usuarios
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Asignar rol de usuario por defecto
            user_role, created = UserRole.objects.get_or_create(
                name='USER',
                defaults={'description': 'Usuario estándar del sistema'}
            )
            user.role = user_role
            
            # Desactivar usuario hasta que verifique su email
            user.is_active = False
            user.save()
            
            # Enviar email de verificación
            send_verification_email(request, user)
            
            messages.success(
                request, 
                '¡Registro exitoso! Por favor, revisa tu correo electrónico para verificar tu cuenta. '
                'El enlace de verificación expirará en 24 horas.'
            )
            return redirect('accounts:login')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
        'page_title': 'Registrarse',
    }
    return render(request, 'accounts/register.html', context)


@login_required
def logout_view(request):
    """
    Vista para cerrar sesión
    """
    # Actualizar el historial de login
    try:
        last_login = LoginHistory.objects.filter(
            user=request.user,
            logout_time__isnull=True
        ).latest('login_time')
        last_login.logout_time = timezone.now()
        last_login.save()
    except LoginHistory.DoesNotExist:
        pass
    
    username = request.user.get_full_name_or_username()
    logout(request)
    messages.info(request, f'Has cerrado sesión correctamente. ¡Hasta pronto, {username}!')
    return redirect('accounts:login')


@login_required
def dashboard_view(request):
    """
    Vista del panel de usuario
    """
    recent_logins = LoginHistory.objects.filter(
        user=request.user
    ).order_by('-login_time')[:5]
    
    # Importar modelos de productos
    from productos.models import Review, Favorite, ActivityLog, Cart, Notification
    
    # Obtener estadísticas del usuario
    user_stats = {
        'total_reviews': Review.objects.filter(user=request.user).count(),
        'total_favorites': Favorite.objects.filter(user=request.user).count(),
        'total_activities': ActivityLog.objects.filter(user=request.user).count(),
        'unread_notifications': Notification.objects.filter(user=request.user, is_read=False).count(),
    }
    
    # Obtener carrito
    cart = None
    cart_total = 0
    try:
        cart = Cart.objects.get(user=request.user)
        cart_total = cart.total_items
    except Cart.DoesNotExist:
        pass
    
    # Obtener actividad reciente
    recent_activities = ActivityLog.objects.filter(
        user=request.user
    ).select_related('producto').order_by('-created_at')[:10]
    
    # Obtener notificaciones no leídas
    recent_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')[:5]
    
    context = {
        'page_title': 'Panel de Usuario',
        'recent_logins': recent_logins,
        'user_stats': user_stats,
        'cart_total': cart_total,
        'recent_activities': recent_activities,
        'recent_notifications': recent_notifications,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def admin_dashboard_view(request):
    """
    Vista del panel de administración (solo para administradores)
    """
    if not request.user.is_admin() and not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('accounts:dashboard')
    
    # Estadísticas
    total_users = CustomUser.objects.count()
    active_users = CustomUser.objects.filter(is_active=True).count()
    admin_users = CustomUser.objects.filter(role__name='ADMIN').count()
    recent_registrations = CustomUser.objects.order_by('-date_joined')[:5]
    recent_logins = LoginHistory.objects.filter(success=True).order_by('-login_time')[:10]
    
    context = {
        'page_title': 'Panel de Administración',
        'total_users': total_users,
        'active_users': active_users,
        'admin_users': admin_users,
        'recent_registrations': recent_registrations,
        'recent_logins': recent_logins,
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def profile_view(request):
    """
    Vista del perfil de usuario
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Manejar cambio de contraseña
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                user.set_password(new_password)
                
                # Enviar notificación de cambio de contraseña por email
                try:
                    send_password_changed_notification(request, user)
                except Exception as e:
                    # Log el error pero no interrumpir el proceso
                    print(f"Error al enviar notificación de cambio de contraseña: {e}")
                
                messages.success(request, 'Contraseña actualizada correctamente.')
            
            user.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            
            # Si cambió la contraseña, actualizar la sesión
            if new_password:
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, user)
            
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = UserProfileForm(instance=request.user)
    
    # Obtener estadísticas del usuario
    from productos.models import Review, Favorite, ActivityLog
    user_stats = {
        'total_reviews': Review.objects.filter(user=request.user).count(),
        'total_favorites': Favorite.objects.filter(user=request.user).count(),
        'total_activities': ActivityLog.objects.filter(user=request.user).count(),
    }
    
    context = {
        'form': form,
        'page_title': 'Mi Perfil',
        'user_stats': user_stats,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
@csrf_protect
def change_password_view(request):
    """
    Vista para cambiar la contraseña del usuario
    Requiere contraseña actual, cierra la sesión y envía notificación por email
    """
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        
        if form.is_valid():
            # Obtener la nueva contraseña
            new_password = form.cleaned_data['new_password']
            
            # Validar la nueva contraseña con los validadores de Django
            # Esto asegura que cumple con TODOS los requisitos antes de cambiar
            try:
                from django.contrib.auth.password_validation import validate_password
                validate_password(new_password, request.user)
            except ValidationError as e:
                # Si la validación falla, mostrar errores y no cambiar la contraseña
                for error in e.messages:
                    messages.error(request, error)
                context = {
                    'form': form,
                    'page_title': 'Cambiar Contraseña',
                }
                return render(request, 'accounts/change_password.html', context)
            
            # Guardar datos del usuario antes de cambiar la contraseña
            user_email = request.user.email
            user_first_name = request.user.first_name
            user_last_name = request.user.last_name
            user_username = request.user.username
            ip_address = get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', 'Desconocido')
            
            # Cambiar la contraseña (solo si pasó todas las validaciones)
            request.user.set_password(new_password)
            request.user.save()
            
            # Enviar email de notificación
            try:
                subject = 'Tu contraseña ha sido actualizada - Kitty Glow'
                html_message = render_to_string('accounts/emails/password_changed_notification.html', {
                    'user': {
                        'username': user_username,
                        'first_name': user_first_name,
                        'last_name': user_last_name,
                        'email': user_email,
                        'get_full_name': f"{user_first_name} {user_last_name}".strip() or user_username,
                    },
                    'change_time': timezone.now().strftime('%d/%m/%Y a las %H:%M:%S'),
                    'ip_address': ip_address,
                    'user_agent': user_agent,
                    'current_year': timezone.now().year,
                })
                
                # Crear versión en texto plano
                plain_message = html_to_plain_text(html_message)
                
                send_html_email(
                    subject=subject,
                    plain_message=plain_message,
                    html_message=html_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user_email],
                    fail_silently=True
                )
            except Exception as e:
                print(f"Error al enviar notificación de cambio de contraseña: {e}")
            
            # Cerrar la sesión del usuario
            logout(request)
            
            # Mensaje de éxito
            messages.success(
                request,
                '¡Contraseña actualizada correctamente! Por seguridad, debes iniciar sesión nuevamente con tu nueva contraseña.'
            )
            return redirect('accounts:login')
        else:
            # Mostrar errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = ChangePasswordForm(user=request.user)
    
    context = {
        'form': form,
        'page_title': 'Cambiar Contraseña',
    }
    return render(request, 'accounts/change_password.html', context)


@login_required
@csrf_protect
def delete_account_view(request):
    """
    Vista para eliminar la cuenta del usuario con período de gracia de 30 días
    Requiere confirmación con contraseña
    """
    # Verificar si la cuenta ya está pendiente de eliminación
    if request.user.is_pending_deletion:
        days_remaining = (request.user.scheduled_deletion_date - timezone.now()).days
        context = {
            'page_title': 'Eliminación Programada',
            'is_pending_deletion': True,
            'scheduled_deletion_date': request.user.scheduled_deletion_date,
            'days_remaining': max(0, days_remaining),
        }
        return render(request, 'accounts/delete_account.html', context)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Acción: Exportar datos
        if action == 'export':
            return export_user_data(request)
        
        # Acción: Desactivar cuenta (período de gracia)
        if action == 'deactivate':
            password = request.POST.get('password')
            confirm_text = request.POST.get('confirm_text', '').strip()
            
            # Verificar la contraseña
            if not request.user.check_password(password):
                messages.error(request, 'La contraseña ingresada es incorrecta.')
                return redirect('accounts:delete_account')
            
            # Verificar el texto de confirmación
            if confirm_text != 'ELIMINAR MI CUENTA':
                messages.error(request, 'Debe escribir exactamente "ELIMINAR MI CUENTA" para confirmar.')
                return redirect('accounts:delete_account')
            
            # Desactivar cuenta y programar eliminación
            request.user.is_pending_deletion = True
            request.user.deletion_requested_at = timezone.now()
            request.user.scheduled_deletion_date = timezone.now() + timedelta(days=30)
            request.user.is_active = False
            request.user.save()
            
            # Guardar la fecha de eliminación antes de cerrar sesión
            scheduled_deletion_date = request.user.scheduled_deletion_date
            
            # Enviar email de notificación
            send_account_deactivation_notification(request.user)
            
            # Cerrar sesión
            logout(request)
            
            messages.warning(
                request,
                f'Tu cuenta ha sido desactivada. Será eliminada permanentemente el '
                f'{scheduled_deletion_date.strftime("%d/%m/%Y")}. '
                f'Puedes cancelar esta acción iniciando sesión antes de esa fecha.'
            )
            return redirect('accounts:login')
        
        # Acción: Eliminar inmediatamente (sin período de gracia)
        if action == 'delete_now':
            password = request.POST.get('password')
            confirm_text = request.POST.get('confirm_text', '').strip()
            confirm_immediate = request.POST.get('confirm_immediate')
            
            # Verificar la contraseña
            if not request.user.check_password(password):
                messages.error(request, 'La contraseña ingresada es incorrecta.')
                return redirect('accounts:delete_account')
            
            # Verificar el texto de confirmación
            if confirm_text != 'ELIMINAR MI CUENTA':
                messages.error(request, 'Debe escribir exactamente "ELIMINAR MI CUENTA" para confirmar.')
                return redirect('accounts:delete_account')
            
            # Verificar confirmación de eliminación inmediata
            if confirm_immediate != 'on':
                messages.error(request, 'Debes confirmar que deseas eliminar inmediatamente.')
                return redirect('accounts:delete_account')
            
            # Guardar información del usuario antes de eliminarlo
            username = request.user.username
            email = request.user.email
            user_id = request.user.id
            
            # Enviar email de notificación
            send_account_deletion_notification(email, username)
            
            # Cerrar sesión antes de eliminar
            logout(request)
            
            # Eliminar el usuario (esto también eliminará datos relacionados según on_delete)
            try:
                CustomUser.objects.filter(id=user_id).delete()
                messages.success(
                    request, 
                    f'Tu cuenta "{username}" ha sido eliminada permanentemente. '
                    'Esperamos verte de nuevo en el futuro.'
                )
            except Exception as e:
                messages.error(request, f'Error al eliminar la cuenta: {str(e)}')
                return redirect('accounts:login')
            
            return redirect('accounts:login')
    
    context = {
        'page_title': 'Eliminar Cuenta',
        'is_pending_deletion': False,
    }
    return render(request, 'accounts/delete_account.html', context)


@login_required
def cancel_account_deletion(request):
    """
    Vista para cancelar la eliminación programada de la cuenta
    """
    if request.user.is_pending_deletion:
        request.user.is_pending_deletion = False
        request.user.deletion_requested_at = None
        request.user.scheduled_deletion_date = None
        request.user.is_active = True
        request.user.save()
        
        messages.success(request, '¡La eliminación de tu cuenta ha sido cancelada exitosamente!')
        return redirect('accounts:profile')
    else:
        messages.info(request, 'No hay ninguna eliminación programada para tu cuenta.')
        return redirect('accounts:profile')


@login_required
def export_user_data(request):
    """
    Vista para exportar todos los datos del usuario en formato JSON
    """
    user = request.user
    
    # Recopilar datos del usuario
    user_data = {
        'informacion_personal': {
            'username': user.username,
            'email': user.email,
            'nombre': user.first_name,
            'apellido': user.last_name,
            'telefono': user.phone_number or '',
            'fecha_nacimiento': user.birth_date.strftime('%d/%m/%Y') if user.birth_date else '',
            'biografia': user.bio,
            'direccion': user.address,
            'ciudad': user.city,
            'pais': user.country,
            'codigo_postal': user.postal_code,
        },
        'informacion_cuenta': {
            'fecha_registro': user.date_joined.strftime('%d/%m/%Y %H:%M:%S'),
            'ultima_actualizacion': user.updated_at.strftime('%d/%m/%Y %H:%M:%S'),
            'email_verificado': user.email_verified,
            'rol': user.get_role_display(),
            'activo': user.is_active,
        },
        'historial_sesiones': [
            {
                'ip': login.ip_address,
                'navegador': login.user_agent,
                'fecha': login.login_time.strftime('%d/%m/%Y %H:%M:%S'),
                'exitoso': login.success,
            }
            for login in user.login_history.all()[:50]  # Últimas 50 sesiones
        ],
    }
    
    # Crear respuesta JSON
    response = HttpResponse(
        json.dumps(user_data, indent=2, ensure_ascii=False),
        content_type='application/json; charset=utf-8'
    )
    response['Content-Disposition'] = f'attachment; filename="datos_usuario_{user.username}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.json"'
    
    return response


@login_required
def user_list_view(request):
    """
    Vista para listar todos los usuarios (solo administradores)
    """
    if not request.user.is_admin() and not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('accounts:dashboard')
    
    users = CustomUser.objects.all().select_related('role').order_by('-date_joined')
    
    context = {
        'users': users,
        'page_title': 'Gestión de Usuarios',
    }
    return render(request, 'accounts/user_list.html', context)


# ============================================
# VERIFICACIÓN DE EMAIL Y RESTABLECIMIENTO DE CONTRASEÑA
# ============================================

def send_verification_email(request, user):
    """
    Envía un email de verificación al usuario
    """
    # Generar token y uid
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Crear enlace de verificación
    verification_link = request.build_absolute_uri(
        f'/accounts/verify-email/{uid}/{token}/'
    )
    
    # Enviar email
    subject = 'Verifica tu cuenta en Kitty Glow'
    html_message = render_to_string('accounts/emails/verification_email.html', {
        'user': user,
        'verification_link': verification_link,
        'current_year': timezone.now().year,
    })
    
    # Crear versión en texto plano
    plain_message = html_to_plain_text(html_message)
    
    send_html_email(
        subject=subject,
        plain_message=plain_message,
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )


def send_login_notification(request, user):
    """
    Envía un email de notificación cuando el usuario inicia sesión
    """
    subject = 'Notificación de inicio de sesión en Kitty Glow'
    html_message = render_to_string('accounts/emails/login_notification.html', {
        'user': user,
        'login_time': timezone.now().strftime('%d/%m/%Y a las %H:%M:%S'),
        'ip_address': get_client_ip(request),
        'user_agent': request.META.get('HTTP_USER_AGENT', 'Desconocido'),
        'current_year': timezone.now().year,
    })
    
    # Crear versión en texto plano
    plain_message = html_to_plain_text(html_message)
    
    send_html_email(
        subject=subject,
        plain_message=plain_message,
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True  # No interrumpir el login si falla el email
    )


def send_password_changed_notification(request, user):
    """
    Envía un email de notificación cuando se cambia la contraseña
    """
    subject = 'Tu contraseña ha sido actualizada - Kitty Glow'
    html_message = render_to_string('accounts/emails/password_changed_notification.html', {
        'user': user,
        'change_time': timezone.now().strftime('%d/%m/%Y a las %H:%M:%S'),
        'ip_address': get_client_ip(request),
        'user_agent': request.META.get('HTTP_USER_AGENT', 'Desconocido'),
        'current_year': timezone.now().year,
    })
    
    # Crear versión en texto plano
    plain_message = html_to_plain_text(html_message)
    
    send_html_email(
        subject=subject,
        plain_message=plain_message,
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True  # No interrumpir el proceso si falla el email
    )


def send_account_deletion_notification(user_email, username):
    """
    Envía un email de notificación cuando se elimina una cuenta
    """
    subject = 'Tu cuenta ha sido eliminada - Kitty Glow'
    html_message = render_to_string('accounts/emails/account_deleted_notification.html', {
        'username': username,
        'deletion_time': timezone.now().strftime('%d/%m/%Y a las %H:%M:%S'),
        'current_year': timezone.now().year,
    })
    
    # Crear versión en texto plano
    plain_message = html_to_plain_text(html_message)
    
    send_html_email(
        subject=subject,
        plain_message=plain_message,
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=True
    )


def send_account_deactivation_notification(user):
    """
    Envía un email de notificación cuando se desactiva una cuenta (período de gracia)
    """
    deletion_date = (timezone.now() + timedelta(days=30)).strftime('%d/%m/%Y')
    
    subject = 'Tu cuenta será eliminada - Kitty Glow'
    html_message = render_to_string('accounts/emails/account_deactivation_notification.html', {
        'user': user,
        'deactivation_time': timezone.now().strftime('%d/%m/%Y a las %H:%M:%S'),
        'deletion_date': deletion_date,
        'current_year': timezone.now().year,
    })
    
    # Crear versión en texto plano
    plain_message = html_to_plain_text(html_message)
    
    send_html_email(
        subject=subject,
        plain_message=plain_message,
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True
    )


def verify_email(request, uidb64, token):
    """
    Verifica el email del usuario usando el token
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, '¡Tu email ha sido verificado exitosamente! Ahora puedes iniciar sesión.')
        return redirect('accounts:login')
    else:
        messages.error(request, 'El enlace de verificación es inválido o ha expirado.')
        return redirect('accounts:login')


@csrf_protect
def password_reset_request(request):
    """
    Vista para solicitar el restablecimiento de contraseña
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = CustomUser.objects.get(email=email)
            
            # Generar token y uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Crear enlace de restablecimiento
            reset_link = request.build_absolute_uri(
                f'/accounts/reset-password/{uid}/{token}/'
            )
            
            # Enviar email
            subject = 'Restablece tu contraseña en Kitty Glow'
            html_message = render_to_string('accounts/emails/password_reset_email.html', {
                'user': user,
                'reset_link': reset_link,
                'current_year': timezone.now().year,
            })
            
            # Crear versión en texto plano
            plain_message = html_to_plain_text(html_message)
            
            send_html_email(
                subject=subject,
                plain_message=plain_message,
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )
            
            messages.success(request, 'Se ha enviado un enlace de restablecimiento a tu correo electrónico.')
            return redirect('accounts:login')
            
        except CustomUser.DoesNotExist:
            # Por seguridad, no revelamos si el email existe o no
            messages.success(request, 'Si el correo electrónico existe, recibirás instrucciones para restablecer tu contraseña.')
            return redirect('accounts:login')
    
    return render(request, 'accounts/password_reset_request.html')


@csrf_protect
def password_reset_confirm(request, uidb64, token):
    """
    Vista para confirmar el restablecimiento de contraseña
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if password1 and password2 and password1 == password2:
                try:
                    # Verificar que la nueva contraseña sea diferente de la anterior
                    if user.check_password(password1):
                        messages.error(request, 'La nueva contraseña debe ser diferente a la contraseña anterior.')
                        context = {
                            'validlink': True,
                            'uidb64': uidb64,
                            'token': token,
                        }
                        return render(request, 'accounts/password_reset_confirm.html', context)
                    
                    # Validar contraseña con los validadores configurados
                    from django.contrib.auth.password_validation import validate_password
                    validate_password(password1, user)
                    
                    user.set_password(password1)
                    user.save()
                    
                    # Enviar notificación de cambio de contraseña por email
                    try:
                        send_password_changed_notification(request, user)
                    except Exception as e:
                        # Log el error pero no interrumpir el proceso
                        print(f"Error al enviar notificación de cambio de contraseña: {e}")
                    
                    messages.success(request, '¡Tu contraseña ha sido restablecida exitosamente! Ahora puedes iniciar sesión.')
                    return redirect('accounts:login')
                except ValidationError as e:
                    for error in e.messages:
                        messages.error(request, error)
            else:
                messages.error(request, 'Las contraseñas no coinciden.')
        
        context = {
            'validlink': True,
            'uidb64': uidb64,
            'token': token,
        }
        return render(request, 'accounts/password_reset_confirm.html', context)
    else:
        messages.error(request, 'El enlace de restablecimiento es inválido o ha expirado.')
        return redirect('accounts:login')


@login_required
@csrf_protect
def active_sessions_view(request):
    """
    Vista para mostrar y gestionar las sesiones activas del usuario
    Permite ver todos los dispositivos con sesión iniciada y cerrar sesiones remotamente
    """
    from .models import ActiveSession
    from django.contrib.sessions.models import Session
    from django.utils import timezone
    from datetime import timedelta
    
    # Obtener la sesión actual
    current_session_key = request.session.session_key
    
    # Limpiar sesiones expiradas (más de 30 días de inactividad)
    expiration_date = timezone.now() - timedelta(days=30)
    ActiveSession.objects.filter(last_activity__lt=expiration_date).delete()
    
    # Obtener todas las sesiones activas del usuario
    active_sessions = ActiveSession.objects.filter(user=request.user).order_by('-last_activity')
    
    # Marcar la sesión actual
    for session in active_sessions:
        session.is_current = (session.session_key == current_session_key)
    
    # Actualizar la sesión actual en la base de datos
    ActiveSession.objects.filter(user=request.user).update(is_current=False)
    if current_session_key:
        ActiveSession.objects.filter(session_key=current_session_key).update(is_current=True)
    
    context = {
        'active_sessions': active_sessions,
        'total_sessions': active_sessions.count(),
        'current_session_key': current_session_key,
        'page_title': 'Sesiones Activas',
    }
    
    return render(request, 'accounts/active_sessions.html', context)


@login_required
@csrf_protect
def close_session_view(request, session_id):
    """
    Cierra una sesión específica por su ID
    No permite cerrar la sesión actual
    """
    from .models import ActiveSession
    from django.contrib.sessions.models import Session
    
    if request.method == 'POST':
        try:
            session = ActiveSession.objects.get(id=session_id, user=request.user)
            
            # No permitir cerrar la sesión actual
            if session.session_key == request.session.session_key:
                messages.error(request, 'No puedes cerrar tu sesión actual desde aquí. Usa el botón "Cerrar Sesión".')
                return redirect('accounts:active_sessions')
            
            # Eliminar la sesión de Django
            try:
                django_session = Session.objects.get(session_key=session.session_key)
                django_session.delete()
            except Session.DoesNotExist:
                pass
            
            # Eliminar el registro de sesión activa
            device_info = session.device_info or 'Dispositivo desconocido'
            session.delete()
            
            messages.success(request, f'Sesión cerrada: {device_info}')
        
        except ActiveSession.DoesNotExist:
            messages.error(request, 'Sesión no encontrada o ya fue cerrada.')
    
    return redirect('accounts:active_sessions')


@login_required
@csrf_protect
def close_all_sessions_view(request):
    """
    Cierra todas las sesiones activas excepto la actual
    """
    from .models import ActiveSession
    from django.contrib.sessions.models import Session
    
    if request.method == 'POST':
        current_session_key = request.session.session_key
        
        # Obtener todas las sesiones excepto la actual
        other_sessions = ActiveSession.objects.filter(
            user=request.user
        ).exclude(session_key=current_session_key)
        
        count = other_sessions.count()
        
        if count == 0:
            messages.info(request, 'No hay otras sesiones activas para cerrar.')
        else:
            # Eliminar las sesiones de Django
            for session in other_sessions:
                try:
                    django_session = Session.objects.get(session_key=session.session_key)
                    django_session.delete()
                except Session.DoesNotExist:
                    pass
            
            # Eliminar los registros de sesiones activas
            other_sessions.delete()
            
            messages.success(request, f'Se han cerrado {count} sesión(es) activa(s).')
    
    return redirect('accounts:active_sessions')


# ============================================
# GESTIÓN DE USUARIOS POR ADMINISTRADOR (AJAX)
# ============================================

@login_required
def user_view_ajax(request, user_id):
    """
    Vista AJAX para obtener los datos de un usuario
    """
    if not request.user.is_admin() and not request.user.is_superuser:
        return JsonResponse({'error': 'No tienes permisos'}, status=403)
    
    try:
        user = CustomUser.objects.select_related('role').get(id=user_id)
        
        # Contar estadísticas
        from productos.models import Review, Favorite
        reviews_count = Review.objects.filter(user=user).count()
        favorites_count = Favorite.objects.filter(user=user).count()
        sessions_count = LoginHistory.objects.filter(user=user, is_active=True).count()
        
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'bio': user.bio,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
            'email_verified': user.email_verified,
            'role_display': user.get_role_display(),
            'date_joined': user.date_joined.strftime('%d/%m/%Y %I:%M %p'),
            'last_login': user.last_login.strftime('%d/%m/%Y %I:%M %p') if user.last_login else None,
            'reviews_count': reviews_count,
            'favorites_count': favorites_count,
            'sessions_count': sessions_count,
        }
        
        return JsonResponse(data)
        
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def user_edit_ajax(request, user_id):
    """
    Vista AJAX para obtener y editar un usuario
    """
    if not request.user.is_admin() and not request.user.is_superuser:
        return JsonResponse({'error': 'No tienes permisos'}, status=403)
    
    try:
        user = CustomUser.objects.select_related('role').get(id=user_id)
        
        if request.method == 'GET':
            # Obtener datos para el formulario
            roles = UserRole.objects.all().order_by('name')
            
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number,
                'bio': user.bio,
                'is_active': user.is_active,
                'email_verified': user.email_verified,
                'role_id': user.role.id if user.role else None,
                'roles': [{'id': role.id, 'name': role.name} for role in roles]
            }
            
            return JsonResponse(data)
        
        elif request.method == 'POST':
            # Actualizar usuario
            try:
                # Validar username único
                username = request.POST.get('username')
                if username != user.username and CustomUser.objects.filter(username=username).exists():
                    return JsonResponse({
                        'success': False,
                        'message': 'El nombre de usuario ya está en uso'
                    })
                
                # Validar email único
                email = request.POST.get('email')
                if email != user.email and CustomUser.objects.filter(email=email).exists():
                    return JsonResponse({
                        'success': False,
                        'message': 'El email ya está en uso'
                    })
                
                # Actualizar campos
                user.username = username
                user.email = email
                user.first_name = request.POST.get('first_name', '')
                user.last_name = request.POST.get('last_name', '')
                user.phone_number = request.POST.get('phone_number', '')
                user.bio = request.POST.get('bio', '')
                user.is_active = request.POST.get('is_active') == 'on'
                user.email_verified = request.POST.get('email_verified') == 'on'
                
                # Actualizar rol
                role_id = request.POST.get('role_id')
                if role_id:
                    user.role = UserRole.objects.get(id=role_id)
                
                user.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Usuario actualizado correctamente'
                })
                
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Error al actualizar: {str(e)}'
                })
        
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def user_delete_ajax(request, user_id):
    """
    Vista AJAX para eliminar un usuario
    """
    if not request.user.is_admin() and not request.user.is_superuser:
        return JsonResponse({'error': 'No tienes permisos'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        user = CustomUser.objects.get(id=user_id)
        
        # Prevenir que el usuario se elimine a sí mismo
        if user.id == request.user.id:
            return JsonResponse({
                'success': False,
                'message': 'No puedes eliminar tu propia cuenta'
            })
        
        # Prevenir eliminar al último superusuario
        if user.is_superuser:
            superuser_count = CustomUser.objects.filter(is_superuser=True).count()
            if superuser_count <= 1:
                return JsonResponse({
                    'success': False,
                    'message': 'No se puede eliminar el último superusuario del sistema'
                })
        
        username = user.username
        user.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Usuario @{username} eliminado correctamente'
        })
        
    except CustomUser.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Usuario no encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al eliminar: {str(e)}'
        }, status=500)
