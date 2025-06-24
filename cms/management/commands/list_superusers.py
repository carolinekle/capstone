from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'List all superusers in the system'

    def handle(self, *args, **options):
        superusers = User.objects.filter(is_superuser=True)
        
        if not superusers.exists():
            self.stdout.write(
                self.style.WARNING('No superusers found in the system.')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS(f'Found {superusers.count()} superuser(s):')
        )
        
        for user in superusers:
            self.stdout.write(f'  - {user.username} ({user.email})')
            if user.is_active:
                self.stdout.write(self.style.SUCCESS('    Status: Active'))
            else:
                self.stdout.write(self.style.ERROR('    Status: Inactive')) 