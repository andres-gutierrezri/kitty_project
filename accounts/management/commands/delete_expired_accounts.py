"""
Comando para eliminar cuentas que han excedido el período de gracia
Este comando debe ejecutarse diariamente mediante un cron job
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import CustomUser
from accounts.views import send_account_deletion_notification


class Command(BaseCommand):
    help = 'Elimina cuentas de usuarios que han excedido el período de gracia de 30 días'

    def handle(self, *args, **options):
        now = timezone.now()
        
        # Buscar cuentas pendientes de eliminación cuya fecha programada ya pasó
        accounts_to_delete = CustomUser.objects.filter(
            is_pending_deletion=True,
            scheduled_deletion_date__lte=now
        )
        
        deleted_count = 0
        
        for user in accounts_to_delete:
            username = user.username
            email = user.email
            
            self.stdout.write(
                self.style.WARNING(
                    f'Eliminando cuenta: {username} ({email})'
                )
            )
            
            # Enviar email de notificación
            send_account_deletion_notification(email, username)
            
            # Eliminar el usuario
            user.delete()
            deleted_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Cuenta eliminada: {username}'
                )
            )
        
        if deleted_count == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    'No hay cuentas pendientes de eliminación.'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n{"="*50}\n'
                    f'Total de cuentas eliminadas: {deleted_count}\n'
                    f'{"="*50}'
                )
            )
