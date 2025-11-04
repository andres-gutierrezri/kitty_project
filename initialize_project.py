#!/usr/bin/env python
"""
Script para inicializar el proyecto Kitty Glow por primera vez.

Ejecuta automáticamente:
1. create_roles - Crea los roles por defecto
2. crear_datos_prueba - Crea productos de ejemplo
3. Muestra información sobre limpieza automática de cuentas

Uso:
    python initialize_project.py
    python initialize_project.py --skip-products
    python initialize_project.py --skip-roles
"""

import os
import sys
import django
import argparse

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitty_glow.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model

User = get_user_model()


def print_header():
    """Imprime el encabezado del script."""
    print('\n' + '='*70)
    print('🐱 INICIALIZANDO PROYECTO KITTY GLOW')
    print('='*70 + '\n')


def print_footer():
    """Imprime el pie del script."""
    print('\n' + '='*70)
    print('✅ INICIALIZACIÓN COMPLETADA')
    print('='*70 + '\n')


def check_if_initialized():
    """Verifica si el proyecto ya fue inicializado."""
    try:
        from accounts.models import UserRole
        from productos.models import Producto
        
        # Verificar si existen roles
        has_roles = UserRole.objects.exists()
        
        # Verificar si existen productos
        has_products = Producto.objects.exists()
        
        return has_roles or has_products
    except Exception:
        return False


def create_roles():
    """Ejecuta el comando create_roles."""
    print('\n' + '-'*70)
    print('📋 Paso 1/2: Creando roles de usuario...')
    print('-'*70 + '\n')
    
    try:
        call_command('create_roles', verbosity=0)
        print('✅ Roles creados exitosamente\n')
    except Exception as e:
        print(f'❌ Error al crear roles: {e}\n')
        print('   Puedes ejecutar manualmente: python manage.py create_roles\n')


def create_sample_products():
    """Ejecuta el comando crear_datos_prueba."""
    print('\n' + '-'*70)
    print('📦 Paso 2/2: Creando productos de prueba...')
    print('-'*70 + '\n')
    
    try:
        call_command('crear_datos_prueba', verbosity=0)
        print('✅ Productos de prueba creados exitosamente\n')
    except Exception as e:
        print(f'❌ Error al crear productos: {e}\n')
        print('   Puedes ejecutar manualmente: python manage.py crear_datos_prueba\n')


def show_additional_info():
    """Muestra información sobre comandos adicionales."""
    print('\n' + '-'*70)
    print('ℹ️  Información adicional')
    print('-'*70 + '\n')
    
    print('📌 Comando de limpieza automática de cuentas:')
    print('   python manage.py delete_expired_accounts\n')
    print('   Este comando elimina cuentas con período de gracia vencido.')
    print('   Recomendación: Configurar en crontab para ejecución diaria.\n')
    print('   Ejemplo de crontab (2:00 AM diario):')
    print('   0 2 * * * cd /ruta/kitty_project && source .venv/bin/activate && python manage.py delete_expired_accounts\n')
    
    # Verificar si existe superusuario
    if not User.objects.filter(is_superuser=True).exists():
        print('⚠️  No se encontró ningún superusuario.')
        print('   Puedes crear uno con:')
        print('   - python manage.py createsuperuser')
        print('   - python create_default_superuser.py (crea admin@kittyglow.com / Admin@2024)\n')


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description='Inicializa el proyecto Kitty Glow con datos por defecto'
    )
    parser.add_argument(
        '--skip-products',
        action='store_true',
        help='Omitir creación de productos de prueba'
    )
    parser.add_argument(
        '--skip-roles',
        action='store_true',
        help='Omitir creación de roles'
    )
    
    args = parser.parse_args()
    
    print_header()
    
    # Verificar si ya se ha inicializado
    if check_if_initialized():
        print('⚠️  El proyecto parece estar ya inicializado.')
        print('   Si deseas reinicializar, los datos existentes se mantendrán.\n')
        response = input('¿Deseas continuar de todas formas? (s/N): ')
        if response.lower() not in ['s', 'si', 'sí', 'yes', 'y']:
            print('Inicialización cancelada.\n')
            return
    
    # 1. Crear roles
    if not args.skip_roles:
        create_roles()
    
    # 2. Crear productos de prueba
    if not args.skip_products:
        create_sample_products()
    
    # 3. Mostrar información sobre comandos adicionales
    show_additional_info()
    
    print_footer()


if __name__ == '__main__':
    main()
