"""
Validadores personalizados para el sistema de autenticación
"""
import re
import unicodedata
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def normalize_text(text):
    """
    Normaliza texto eliminando acentos y convirtiendo a minúsculas
    Ejemplo: 'Andrés' -> 'andres'
    """
    if not text:
        return ''
    # Normalizar unicode (NFD separa caracteres base de diacríticos)
    nfd = unicodedata.normalize('NFD', text)
    # Filtrar solo caracteres ASCII (elimina acentos)
    without_accents = ''.join(c for c in nfd if unicodedata.category(c) != 'Mn')
    return without_accents.lower()


class CustomPasswordValidator:
    """
    Validador personalizado de contraseñas con los siguientes requisitos:
    - Entre 8 y 20 caracteres
    - Al menos una letra mayúscula
    - Al menos una letra minúscula
    - Al menos un carácter especial (!@#$%^&*.-_+...)
    - Sin espacios ni emojis
    - No similar al nombre de usuario, email, nombre o apellido
    """
    
    def validate(self, password, user=None):
        """
        Valida que la contraseña cumpla con todos los requisitos
        """
        # Verificar longitud
        if len(password) < 8:
            raise ValidationError(
                _("La contraseña debe tener al menos 8 caracteres."),
                code='password_too_short',
            )
        
        if len(password) > 20:
            raise ValidationError(
                _("La contraseña no puede tener más de 20 caracteres."),
                code='password_too_long',
            )
        
        # Verificar que tenga al menos una letra mayúscula
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos una letra mayúscula."),
                code='password_no_upper',
            )
        
        # Verificar que tenga al menos una letra minúscula
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos una letra minúscula."),
                code='password_no_lower',
            )
        
        # Verificar que tenga al menos un carácter especial
        # Caracteres permitidos: !@#$%^&*.-_+(){}[]:;<>?,/\|~`
        if not re.search(r'[!@#$%^&*.\-_+(){}[\]:;<>?,/\\|~`]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos un carácter especial (!@#$%^&*.-_+(){}[]:;<>?,/\\|~)."),
                code='password_no_special',
            )
        
        # Verificar que no tenga espacios
        if ' ' in password:
            raise ValidationError(
                _("La contraseña no puede contener espacios."),
                code='password_has_spaces',
            )
        
        # Verificar que no tenga emojis u otros caracteres Unicode no permitidos
        # Solo permitir caracteres ASCII imprimibles
        if not all(32 <= ord(char) <= 126 for char in password):
            raise ValidationError(
                _("La contraseña contiene caracteres no permitidos (como emojis)."),
                code='password_invalid_chars',
            )
        
        # Verificar que no tenga caracteres ni números consecutivos (1.8)
        # Verificar 3 o más caracteres idénticos consecutivos (aaa, 111, AAA)
        if re.search(r'(.)\1{2,}', password):
            raise ValidationError(
                _("La contraseña no puede contener tres o más caracteres idénticos consecutivos (ejemplo: aaa, 111)."),
                code='password_consecutive_chars',
            )
        
        # Verificar secuencias alfabéticas consecutivas (abc, xyz, ABC, XYZ)
        for i in range(len(password) - 2):
            char1 = password[i].lower()
            char2 = password[i + 1].lower()
            char3 = password[i + 2].lower()
            
            # Verificar si son letras consecutivas
            if char1.isalpha() and char2.isalpha() and char3.isalpha():
                if ord(char2) == ord(char1) + 1 and ord(char3) == ord(char2) + 1:
                    raise ValidationError(
                        _("La contraseña no puede contener secuencias alfabéticas consecutivas (ejemplo: abc, xyz)."),
                        code='password_consecutive_letters',
                    )
        
        # Verificar secuencias numéricas consecutivas (123, 789)
        for i in range(len(password) - 2):
            if password[i].isdigit() and password[i + 1].isdigit() and password[i + 2].isdigit():
                num1 = int(password[i])
                num2 = int(password[i + 1])
                num3 = int(password[i + 2])
                
                if num2 == num1 + 1 and num3 == num2 + 1:
                    raise ValidationError(
                        _("La contraseña no puede contener secuencias numéricas consecutivas (ejemplo: 123, 789)."),
                        code='password_consecutive_numbers',
                    )
        
        # Verificar que no sea similar al username, email, nombre o apellido
        if user:
            # Normalizar la contraseña (sin acentos, en minúsculas)
            password_normalized = normalize_text(password)
            
            # Lista de atributos a verificar
            user_attributes = []
            
            # Username
            if hasattr(user, 'username') and user.username:
                user_attributes.append(normalize_text(user.username))
            
            # Email (completo y parte local)
            if hasattr(user, 'email') and user.email:
                email_normalized = normalize_text(user.email)
                user_attributes.append(email_normalized)
                # Agregar la parte local del email (antes del @)
                if '@' in user.email:
                    email_local = user.email.split('@')[0]
                    user_attributes.append(normalize_text(email_local))
            
            # Nombre
            if hasattr(user, 'first_name') and user.first_name:
                user_attributes.append(normalize_text(user.first_name))
            
            # Apellido
            if hasattr(user, 'last_name') and user.last_name:
                user_attributes.append(normalize_text(user.last_name))
            
            # Verificar similitud
            for attribute in user_attributes:
                if not attribute or len(attribute) < 3:
                    continue
                
                # Verificar si la contraseña contiene el atributo
                if attribute in password_normalized:
                    raise ValidationError(
                        _("La contraseña no puede contener tu nombre de usuario, email, nombre o apellido."),
                        code='password_too_similar',
                    )
                
                # Verificar si el atributo contiene la contraseña
                if password_normalized in attribute:
                    raise ValidationError(
                        _("La contraseña es demasiado similar a tu información personal."),
                        code='password_too_similar',
                    )
    
    def get_help_text(self):
        """
        Retorna el texto de ayuda para el validador
        """
        return _(
            "Tu contraseña debe cumplir con los siguientes requisitos:\n"
            "• Entre 8 y 20 caracteres\n"
            "• Al menos una letra mayúscula (A-Z)\n"
            "• Al menos una letra minúscula (a-z)\n"
            "• Al menos un carácter especial (!@#$%^&*.-_+...)\n"
            "• Sin espacios ni emojis\n"
            "• Sin caracteres ni números consecutivos (aaa, 111, abc, 123)\n"
            "• No similar a tu nombre de usuario, email, nombre o apellido"
        )
