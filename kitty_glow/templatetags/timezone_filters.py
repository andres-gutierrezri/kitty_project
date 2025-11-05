"""
========================================
FILTROS DE ZONA HORARIA
Archivo: timezone_filters.py
========================================

Filtros personalizados de Django para convertir y formatear
fechas/horas en la zona horaria local del proyecto.
"""

from django import template
from django.utils import timezone
from django.conf import settings
import pytz

register = template.Library()


@register.filter(name='localtime')
def localtime_filter(value):
    """
    Convierte una fecha/hora UTC a la zona horaria local del proyecto.
    
    Uso en templates:
        {{ fecha|localtime }}
    
    Args:
        value: datetime object (timezone-aware o naive)
    
    Returns:
        datetime object en la zona horaria local
    """
    if value is None:
        return None
    
    # Si no tiene zona horaria, asumimos UTC
    if timezone.is_naive(value):
        value = timezone.make_aware(value, timezone.utc)
    
    # Convertir a la zona horaria local configurada
    local_tz = pytz.timezone(settings.TIME_ZONE)
    return value.astimezone(local_tz)


@register.filter(name='local_datetime')
def local_datetime_filter(value, format_string='%d/%m/%Y %I:%M %p'):
    """
    Convierte y formatea una fecha/hora a la zona horaria local.
    
    Uso en templates:
        {{ fecha|local_datetime }}
        {{ fecha|local_datetime:"%d de %B de %Y, %I:%M %p" }}
    
    Args:
        value: datetime object
        format_string: string con formato strftime (opcional)
    
    Returns:
        string con la fecha/hora formateada
    """
    if value is None:
        return ''
    
    # Convertir a zona horaria local
    local_time = localtime_filter(value)
    
    if local_time is None:
        return ''
    
    # Formatear según el string proporcionado
    try:
        return local_time.strftime(format_string)
    except:
        return str(local_time)


@register.filter(name='local_date')
def local_date_filter(value, format_string='%d/%m/%Y'):
    """
    Convierte y formatea solo la fecha (sin hora) a la zona horaria local.
    
    Uso en templates:
        {{ fecha|local_date }}
        {{ fecha|local_date:"%d de %B de %Y" }}
    
    Args:
        value: datetime object
        format_string: string con formato strftime (opcional)
    
    Returns:
        string con la fecha formateada
    """
    return local_datetime_filter(value, format_string)


@register.filter(name='local_time')
def local_time_filter(value, format_string='%I:%M %p'):
    """
    Convierte y formatea solo la hora (sin fecha) a la zona horaria local.
    
    Uso en templates:
        {{ fecha|local_time }}
        {{ fecha|local_time:"%H:%M:%S" }}
    
    Args:
        value: datetime object
        format_string: string con formato strftime (opcional)
    
    Returns:
        string con la hora formateada
    """
    return local_datetime_filter(value, format_string)


@register.filter(name='timezone_name')
def timezone_name_filter(value=None):
    """
    Retorna el nombre de la zona horaria local.
    
    Uso en templates:
        {{ None|timezone_name }}  o  {{ some_date|timezone_name }}
    
    Returns:
        string con el nombre de la zona horaria (ej: "America/Bogota")
    """
    return settings.TIME_ZONE


@register.filter(name='timezone_offset')
def timezone_offset_filter(value=None):
    """
    Retorna el offset de la zona horaria local (ej: "-05:00").
    
    Uso en templates:
        {{ None|timezone_offset }}  o  {{ some_date|timezone_offset }}
    
    Returns:
        string con el offset de la zona horaria
    """
    local_tz = pytz.timezone(settings.TIME_ZONE)
    now = timezone.now().astimezone(local_tz)
    offset = now.strftime('%z')
    # Formatear como "-05:00" en lugar de "-0500"
    if len(offset) == 5:
        return f"{offset[:3]}:{offset[3:]}"
    return offset


@register.simple_tag(name='current_timezone')
def current_timezone_tag():
    """
    Template tag que retorna la zona horaria actual.
    
    Uso en templates:
        {% current_timezone %}
    
    Returns:
        string con la zona horaria configurada
    """
    return settings.TIME_ZONE


@register.simple_tag(name='now_local')
def now_local_tag(format_string='%d/%m/%Y %I:%M %p'):
    """
    Template tag que retorna la fecha/hora actual en zona horaria local.
    
    Uso en templates:
        {% now_local %}
        {% now_local "%d de %B de %Y, %I:%M %p" %}
    
    Args:
        format_string: string con formato strftime (opcional)
    
    Returns:
        string con la fecha/hora actual formateada
    """
    now = timezone.now()
    return local_datetime_filter(now, format_string)

