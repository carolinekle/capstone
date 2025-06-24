from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Reset password for a superuser'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the superuser')
        parser.add_argument('--password', type=str, help='New password (will prompt if not provided)')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']

        try:
            user = User.objects.get(username=username, is_superuser=True)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Superuser "{username}" does not exist.')
            )
            return

        # Prompt for password if not provided
        if not password:
            password = input('Enter new password: ')
            password_confirm = input('Confirm new password: ')
            if password != password_confirm:
                self.stdout.write(
                    self.style.ERROR('Passwords do not match.')
                )
                return

        # Set the new password
        user.set_password(password)
        user.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully reset password for superuser "{username}"')
        ) 