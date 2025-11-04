"""
Middleware para rastrear sesiones activas de usuarios
"""
from django.utils import timezone
from .models import ActiveSession


class ActiveSessionMiddleware:
    """
    Middleware que rastrea y actualiza sesiones activas
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Procesar la solicitud
        response = self.get_response(request)
        
        # Si el usuario está autenticado y tiene sesión
        if request.user.is_authenticated and hasattr(request, 'session'):
            session_key = request.session.session_key
            
            if session_key:
                # Obtener información del cliente
                ip_address = self.get_client_ip(request)
                user_agent = request.META.get('HTTP_USER_AGENT', '')
                
                # Actualizar o crear sesión activa
                session, created = ActiveSession.objects.get_or_create(
                    session_key=session_key,
                    defaults={
                        'user': request.user,
                        'ip_address': ip_address,
                        'user_agent': user_agent,
                        'device_info': self.extract_device_info(user_agent),
                        'browser_info': self.extract_browser_info(user_agent),
                    }
                )
                
                # Si no se creó, actualizar última actividad
                if not created:
                    session.last_activity = timezone.now()
                    session.user = request.user  # Asegurar que el usuario sea correcto
                    session.ip_address = ip_address
                    session.save(update_fields=['last_activity', 'user', 'ip_address'])
        
        return response
    
    @staticmethod
    def get_client_ip(request):
        """Obtiene la dirección IP del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @staticmethod
    def extract_device_info(user_agent):
        """Extrae información básica del dispositivo"""
        user_agent_lower = user_agent.lower()
        
        if 'iphone' in user_agent_lower:
            return 'iPhone'
        elif 'ipad' in user_agent_lower:
            return 'iPad'
        elif 'android' in user_agent_lower:
            if 'mobile' in user_agent_lower:
                return 'Android Phone'
            else:
                return 'Android Tablet'
        elif 'windows' in user_agent_lower:
            return 'Windows PC'
        elif 'mac os' in user_agent_lower or 'macos' in user_agent_lower:
            return 'Mac'
        elif 'linux' in user_agent_lower:
            return 'Linux PC'
        else:
            return 'Dispositivo Desconocido'
    
    @staticmethod
    def extract_browser_info(user_agent):
        """Extrae información del navegador"""
        user_agent_lower = user_agent.lower()
        
        if 'edge' in user_agent_lower or 'edg/' in user_agent_lower:
            return 'Microsoft Edge'
        elif 'chrome' in user_agent_lower and 'edg' not in user_agent_lower:
            return 'Google Chrome'
        elif 'firefox' in user_agent_lower:
            return 'Mozilla Firefox'
        elif 'safari' in user_agent_lower and 'chrome' not in user_agent_lower:
            return 'Safari'
        elif 'opera' in user_agent_lower or 'opr/' in user_agent_lower:
            return 'Opera'
        else:
            return 'Navegador Desconocido'
