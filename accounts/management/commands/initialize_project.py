"""
Comando para inicializar el proyecto Kitty Glow por primera vez.

Ejecuta automáticamente:
1. create_roles - Crea los roles por defecto
2. crear_datos_prueba - Crea 15 productos de ejemplo
3. Configura limpieza automática de cuentas expiradas

Uso:
    python manage.py initialize_project
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.contrib.auth import get_user_model
import sys

User = get_user_model()


class Command(BaseCommand):
    help = 'Inicializa el proyecto Kitty Glow con datos por defecto'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-products',
            action='store_true',
            help='Omitir creación de productos de prueba',
        )
        parser.add_argument(
            '--skip-roles',
            action='store_true',
            help='Omitir creación de roles',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '='*70))
        self.stdout.write(self.style.SUCCESS('🐱 INICIALIZANDO PROYECTO KITTY GLOW'))
        self.stdout.write(self.style.SUCCESS('='*70 + '\n'))

        # Verificar si ya se ha inicializado
        if self._check_if_initialized() and not options.get('verbosity', 1) > 1:
            self.stdout.write(self.style.WARNING(
                '⚠️  El proyecto parece estar ya inicializado.\n'
                '   Si deseas reinicializar, ejecuta: python manage.py initialize_project --verbosity=2\n'
            ))
            response = input('¿Deseas continuar de todas formas? (s/N): ')
            if response.lower() not in ['s', 'si', 'sí', 'yes', 'y']:
                self.stdout.write(self.style.WARNING('Inicialización cancelada.\n'))
                return

        # 1. Crear roles
        if not options['skip_roles']:
            self._create_roles()
        
        # 2. Crear productos de prueba
        if not options['skip_products']:
            self._create_sample_products()
        
        # 3. Mostrar información sobre comandos adicionales
        self._show_additional_info()

        self.stdout.write(self.style.SUCCESS('\n' + '='*70))
        self.stdout.write(self.style.SUCCESS('✅ INICIALIZACIÓN COMPLETADA'))
        self.stdout.write(self.style.SUCCESS('='*70 + '\n'))

    def _check_if_initialized(self):
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

    def _create_roles(self):
        """Ejecuta el comando create_roles."""
        self.stdout.write('\n' + '-'*70)
        self.stdout.write(self.style.HTTP_INFO('📋 Paso 1/2: Creando roles de usuario...'))
        self.stdout.write('-'*70 + '\n')
        
        try:
            call_command('create_roles', verbosity=0)
            self.stdout.write(self.style.SUCCESS('✅ Roles creados exitosamente\n'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error al crear roles: {e}\n'))
            self.stdout.write(self.style.WARNING('   Puedes ejecutar manualmente: python manage.py create_roles\n'))

    def _create_sample_products(self):
        """Ejecuta el comando crear_datos_prueba."""
        self.stdout.write('\n' + '-'*70)
        self.stdout.write(self.style.HTTP_INFO('📦 Paso 2/2: Creando productos de prueba...'))
        self.stdout.write('-'*70 + '\n')
        
        try:
            call_command('crear_datos_prueba', verbosity=0)
            self.stdout.write(self.style.SUCCESS('✅ Productos de prueba creados exitosamente\n'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error al crear productos: {e}\n'))
            self.stdout.write(self.style.WARNING('   Puedes ejecutar manualmente: python manage.py crear_datos_prueba\n'))

    def _show_additional_info(self):
        """Muestra información sobre comandos adicionales."""
        self.stdout.write('\n' + '-'*70)
        self.stdout.write(self.style.HTTP_INFO('ℹ️  Información adicional'))
        self.stdout.write('-'*70 + '\n')
        
        self.stdout.write(self.style.WARNING(
            '📌 Comando de limpieza automática de cuentas:\n'
            '   python manage.py delete_expired_accounts\n\n'
            '   Este comando elimina cuentas con período de gracia vencido.\n'
            '   Recomendación: Configurar en crontab para ejecución diaria.\n\n'
            '   Ejemplo de crontab (2:00 AM diario):\n'
            '   0 2 * * * cd /ruta/kitty_project && source .venv/bin/activate && python manage.py delete_expired_accounts\n'
        ))
        
        # Verificar si existe superusuario
        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.WARNING(
                '\n⚠️  No se encontró ningún superusuario.\n'
                '   Puedes crear uno con:\n'
                '   - python manage.py createsuperuser\n'
                '   - python create_default_superuser.py (crea admin@kittyglow.com / Admin@2024)\n'
            ))
