"""
Comando para crear los roles iniciales del sistema
"""
from django.core.management.base import BaseCommand
from accounts.models import UserRole


class Command(BaseCommand):
    help = 'Crea los roles iniciales del sistema'
    
    def handle(self, *args, **kwargs):
        roles_data = [
            {
                'name': 'ADMIN',
                'description': 'Administrador del sistema con todos los permisos',
                'permissions': {
                    'can_manage_users': True,
                    'can_delete_users': True,
                    'can_view_reports': True,
                    'can_manage_roles': True,
                }
            },
            {
                'name': 'USER',
                'description': 'Usuario estándar del sistema',
                'permissions': {
                    'can_view_profile': True,
                    'can_edit_profile': True,
                }
            },
            {
                'name': 'MODERATOR',
                'description': 'Moderador con permisos limitados de administración',
                'permissions': {
                    'can_view_users': True,
                    'can_edit_users': True,
                    'can_view_reports': True,
                }
            },
            {
                'name': 'GUEST',
                'description': 'Invitado con permisos muy limitados',
                'permissions': {
                    'can_view_profile': True,
                }
            },
        ]
        
        created_count = 0
        existing_count = 0
        
        for role_data in roles_data:
            role, created = UserRole.objects.get_or_create(
                name=role_data['name'],
                defaults={
                    'description': role_data['description'],
                    'permissions': role_data['permissions']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Rol creado: {role.get_name_display()}')
                )
            else:
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(f'○ Rol ya existe: {role.get_name_display()}')
                )
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Resumen:'))
        self.stdout.write(self.style.SUCCESS(f'  - Roles creados: {created_count}'))
        self.stdout.write(self.style.WARNING(f'  - Roles existentes: {existing_count}'))
        self.stdout.write(self.style.SUCCESS(f'  - Total: {created_count + existing_count}'))
